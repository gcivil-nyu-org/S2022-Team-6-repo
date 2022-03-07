from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.circle, name='circle'),
    path('current/<str:username>/<str:circle_id>/',
         views.current_circle, name='current'),
    path('create/<str:username>', views.create, name='create'),
    path('create/notifications/<str:username>', views.notify, name='notify'),
    #     path('remove/<str:circleid>/<str:username>/',
    #          views.remove_user, name='remove')
]
