from django.urls import path
from . import views

app_name = 'monitor'
urlpatterns = [
    path("<str:username>/", views.base, name="monitor"),
]
