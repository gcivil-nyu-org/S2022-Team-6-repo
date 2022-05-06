from django.urls import path
from . import views

app_name = "circle"
urlpatterns = [
    path("<str:username>/<str:query>/", views.circle, name="dashboard"),
    path(
        "current/<str:username>/<str:circle_id>/",
        views.current_circle,
        name="user_circle",
    ),
    path("create", views.create, name="create"),
    path("create/notifications/<str:username>/", views.notify, name="notify"),
    path(
        "exit/<str:username>/<str:circle_id>/",
        views.exit_circle,
        name="exitcircle",
    ),
    path(
        "deletecircle/<str:username>/<str:circle_id>/",
        views.delete_circle,
        name="deletecircle",
    ),
    path(
        "editpermission/<str:username>/<str:circle_id>/",
        views.edit_permission,
        name="editpermission",
    ),
    path(
        "request_url/<str:display_code>",
        views.request_url,
        name="request_url",
    ),
]
