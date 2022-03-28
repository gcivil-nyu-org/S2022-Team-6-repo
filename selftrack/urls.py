from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>", views.selftrack, name="selftrack"),
    path("save/<str:username>", views.selftracksave, name="selftracksave"),
]
