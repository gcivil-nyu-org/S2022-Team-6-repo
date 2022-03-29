from django.urls import path
from . import views

app_name = "monitor"
urlpatterns = [
    path("", views.base, name="user_monitor"),
]
