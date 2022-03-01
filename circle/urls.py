from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.circle, name='circle'),
    path('current/<str:username>/<str:circleid>/',
         views.current_circle, name='current'),
    path('create/<str:username>', views.create, name='create')
]
