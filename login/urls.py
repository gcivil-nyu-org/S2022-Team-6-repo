from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = "login"
urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("errorpage/", views.error, name="error"),
    path("logout/", views.logout, name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="login/password_reset.html",
            email_template_name="login/password_reset_email.html",
            success_url=reverse_lazy("login:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="login/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="login/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="login/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("<str:username>", views.profile_view, name="profile"),
    path("<str:username>/profile", views.user_profile, name="user_profile"),
    path("<str:username>/privacy", views.user_privacy, name="privacy"),
    path("<str:username>/password", views.user_change_password, name="change_password"),
    path("settings/<str:username>/<str:page>", views.settings, name="settings"),
]
