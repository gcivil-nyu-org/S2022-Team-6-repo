from django.urls import path
from . import views

app_name = "alert"

urlpatterns = [
    path("<str:username>/", views.alert_user, name="alert_user"),
]
