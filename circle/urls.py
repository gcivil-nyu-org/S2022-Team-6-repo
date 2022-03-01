from django.urls import path
from . import views

urlpatterns = [
    path('', views.circle, name='circle'),
    path('current/<str:pk>/', views.current_circle, name='signin'),
    path('create/', views.create, name='create')
]
