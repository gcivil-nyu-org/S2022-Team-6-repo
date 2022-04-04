from django.urls import path
from . import views

app_name = "selftracking"

urlpatterns = [
    path("<str:username>/", views.selftrack, name="selftrack"),
]
