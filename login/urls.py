from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("errorpage/", views.error, name="error"),
    path("logout/", views.logout, name="logout"),
    path("<str:username>", views.profile_view, name="profile"),
    path("<str:username>/profile", views.user_profile, name="user_profile"),
    path("<str:username>/privacy", views.user_privacy, name="privacy"),
    path("<str:username>/password", views.user_change_password, name="change_password"),
    path("settings/<str:username>/<str:page>", views.settings, name="settings"),
]
