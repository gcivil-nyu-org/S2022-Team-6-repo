from django.urls import path
from . import views
#app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.createuser, name='createuser'),
    path('login/', views.login, name='login')
]
