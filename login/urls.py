from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("errorpage/", views.error, name="error"),
    path("logout/", views.logout, name="logout"),
    path("profile/<str:username>/", views.profile, name="profile"),
]
