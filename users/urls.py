from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:secret>", views.complete_verification, name="complete_verification"
    ),
    path("login/github", views.github_login, name="github_login"),
    path("login/github/callback", views.github_callback, name="github_callback"),
    path("login/gmail", views.gmail_login, name="gmail_login"),
    path("login/gmail/callback", views.gmail_callback, name="gmail_callback"),
]
