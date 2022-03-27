from django.urls import path
from . import views

app_name = "monitor"
urlpatterns = [
    path("<str:user_enc>/", views.base, name="user_monitor"),
]
