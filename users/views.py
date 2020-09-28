from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms


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
