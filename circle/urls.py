from django.urls import path
from . import views

app_name = 'circle'
urlpatterns = [
    path("<str:username>/", views.circle, name="dashboard"),
    path(
        "current/<str:username>/<str:circle_id>/", views.current_circle, name="user_circle"
    ),
    path("create/<str:username>/", views.create, name="create"),
    path("create/notifications/<str:username>/", views.notify, name="notify")
]
