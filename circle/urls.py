from django.urls import path
from . import views

app_name = 'circle'
urlpatterns = [
    path("<str:user_enc>/", views.circle, name="dashboard"),
    path(
        "current/<str:user_enc>/<str:username>/<str:circle_id>/", views.current_circle, name="user_circle"
    ),
    path("create/<str:user_enc>/", views.create, name="create"),
    path("create/notifications/<str:user_enc>/", views.notify, name="notify")
]
