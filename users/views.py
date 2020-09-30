import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from . import forms, models


# does the same thing as the LoginView1 class
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        print("cleaned data= ", form.cleaned_data)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        # super takes us to the success url automatically
        # we don't have to redirect


# Create your views here.
# instead of generic view you could also extend from LoginView/FormView
# however it asks for username and not email
class LoginView1(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(
            request,
            "users/login.html",
            {"form": form},
        )

    def post(self, request):
        form = forms.LoginForm(request.POST)
        # print(form)

        # we cannot just make a post requesr for any valid email and pass
        # we need to check if user actually exists in database
        # hence we have to throw custom errors as done in users.forms
        if form.is_valid():
            print("cleaned data= ", form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # redirect user
                return redirect(reverse("core:home"))

        return render(
            request,
            "users/login.html",
            {"form": form},
        )


def log_out(request):
    # django takes care of everything by alling the below function
    print("log out request", request)
    logout(request)
    return redirect(reverse("core:home"))


# form.cleaned_data cleans all the fields, including those we declared
# like clean_email and clean_password in users.forms

# same thing as above
"""def login_view(request):
    if request.method == "GET":
        pass

    elif request.method == "POST":
        pass
"""


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    # initial is used for pre-populating fields
    # initial = {
    #     "first_name": "Harjot",
    #     "last_name": "Singh",
    #     "email": "harjot@gmail.com",
    # }

    def form_valid(self, form):
        print("cleaned data= ", form.cleaned_data)
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

    # super takes us to the success url automatically
    # we don't have to redirect


def complete_verification(request, secret):
    print(secret)
    try:
        user = models.User.objects.get(email_secret=secret)
        print(user)
        user.email_verified = True

        # delete the secret key now
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # user does not exist with that email
        # to do: throw error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user",
    )


class GithubException(Exception):
    pass


# called after user accepts authentication request in github
# gives back a code
# which is used to get an access token
def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")

        # github returns us an access code to access the API
        print(request.GET)
        code = request.GET.get("code", None)

        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            print(result.json())
            result_json = result.json()
            error = result_json.get("error", None)
            # if more than 10 mins have passed we get error
            # which is why we have to check
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                print(profile_json)
                username = profile_json.get("login", None)
                email = profile_json.get("email", None)
                if username is not None and email is not None:
                    name = profile_json.get("name")
                    bio = profile_json.get("bio")
                    avatar_url = profile_json.get("avatar_url")

                    # checking if user with the same mail exists
                    try:
                        user = models.User.objects.get(email=email)
                        # user exists send back to home
                        if user.login_method == models.User.LOGIN_GITHUB:
                            # user is trying to log in
                            print(
                                user,
                                "is is signed up with github and is trying to log in",
                            )
                            login(request, user)
                        else:
                            print(
                                user,
                                "is is not signed up with github and is trying to log in",
                            )
                            raise GithubException()

                    except models.User.DoesNotExist:
                        # create new user
                        new_user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )

                        # user should not be able to login wth any password now
                        # since he is logging in with github
                        new_user.set_unusable_password()
                        new_user.save()

                        if avatar_url is not None:
                            photo_request = requests.get(avatar_url)

                            # the below method comes from ImageField
                            # takes in file name and content
                            # content is zeroes and ones
                            # which photo_request.content will give

                            photo_content = ContentFile(photo_request.content)
                            new_user.avatar.save(f"{email}-avatar.jpeg", photo_content)
                        print(
                            new_user,
                            "is is now signing with github and is trying to log in",
                        )
                        login(request, new_user)

                    # user exists or does not send to hone in any case
                    return redirect(reverse("core:home"))
                else:
                    print("unable to get users username or password")
                    return redirect(reverse("users:login"))

        else:
            # no access token returned
            # so dont log user in
            # and send back to home
            raise GithubException()
    except GithubException:
        print("github exception raised")
        return redirect(reverse("core:home"))


def gmail_login(request):
    print("gmail login request", request)
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/gmail/callback"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope=email%20profile&response_type=code",
    )


class GmailException(BaseException):
    pass


def gmail_callback(request):
    print("gmail login callback request = ", request)
    auth_code = request.GET.get("code", None)
    error = request.GET.get("error")
    print("auth code= ", auth_code)
    print("error= ", error)
    try:
        client_id = os.environ.get("GMAIL_CLIENT_ID")
        client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
        redirect_url = "http://127.0.0.1:8000/users/login/gmail/callback"
        if auth_code is not None:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": auth_code,
                "redirect_uri": redirect_url,
                "grant_type": "authorization_code",
            }
            access_token_result = requests.post(
                "https://oauth2.googleapis.com/token",
                data=data,
            )
            # print(access_token_result)
            # print(access_token_result.content)
            print("access token result json= ", access_token_result.json())
            access_token_json = access_token_result.json()
            error = access_token_json.get("error")
            print("error in getting access token= ", error)

            if error is not None:
                raise GmailException()
            else:
                # continue with google api
                access_token = access_token_json.get("access_token")
                print("error not occurred access token= ", access_token)

                profile_request = requests.get(
                    f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
                )

                print("profile request= ", profile_request.json())
                profile_json = profile_request.json()
                email = profile_json.get("email", None)
                if email is not None:
                    name = profile_json.get("name")
                    avatar_url = profile_json.get("picture", None)

                    # checking if user with the same mail exists
                    try:
                        user = models.User.objects.get(email=email)
                        # user exists send back to home
                        if user.login_method == models.User.LOGIN_GMAIL:
                            # user is trying to log in
                            print(
                                user,
                                "is is signed up with gmail and is trying to log in",
                            )
                            login(request, user)
                        else:
                            print(
                                user,
                                "is is not signed up with gmail and is trying to log in",
                            )
                            raise GmailException()

                    except models.User.DoesNotExist:
                        # create new user
                        new_user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            login_method=models.User.LOGIN_GMAIL,
                            email_verified=True,
                        )

                        # user should not be able to login wth any password now
                        # since he is logging in with gmail
                        new_user.set_unusable_password()
                        new_user.save()

                        if avatar_url is not None:
                            photo_request = requests.get(avatar_url)

                            # the below method comes from ImageField
                            # takes in file name and content
                            # content is zeroes and ones
                            # which photo_request.content will give

                            photo_content = ContentFile(photo_request.content)
                            new_user.avatar.save(f"{email}-avatar.jpeg", photo_content)

                        print(
                            new_user,
                            "is is now signing with gmail and is trying to log in",
                        )
                        login(request, new_user)

                    # user exists or does not send to hone in any case
                    return redirect(reverse("core:home"))
                else:
                    print("unable to get users username or password")
                    return redirect(reverse("users:login"))
        else:
            # no access token returned
            # so dont log user in
            # and send back to home
            raise GmailException()
    except GmailException:
        print("Gmail exception raised")
        return redirect(reverse("core:home"))
