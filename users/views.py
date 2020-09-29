from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
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
    initial = {
        "first_name": "Harjot",
        "last_name": "Singh",
        "email": "harjot@gmail.com",
    }

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