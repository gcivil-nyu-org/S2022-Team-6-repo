from django.urls import path
from . import views

app_name = "circle"
urlpatterns = [
    path("<str:user_enc>/", views.circle, name="dashboard"),
    path(
        "current/<str:user_enc>/<str:username>/<str:circle_id>/",
        views.current_circle,
        name="user_circle",
    ),
    path("create/<str:user_enc>/", views.create, name="create"),
    path("create/notifications/<str:user_enc>/", views.notify, name="notify"),
    path("exit/<str:username>/<str:circle_id>/<str:user_enc>", views.exit_circle, name="exitcircle"),
    path("deletecircle/<str:username>/<str:circle_id>/<str:user_enc>", views.delete_circle, name="deletecircle"),
]
