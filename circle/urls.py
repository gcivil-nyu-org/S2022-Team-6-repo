from django.urls import path
from . import views

urlpatterns = [
    path('', views.circle, name='circle'),
    path('current/<str:pk>/', views.current_circle, name='current'),
    path('create/', views.create, name='create')
]
