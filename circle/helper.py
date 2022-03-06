from .models import Circle, CircleUser, CirclePolicy, Policy, RequestCircle
from login.models import UserData


def get_notifications(username):
    admin_user_data = CircleUser.objects.filter(
        username=username, is_admin=True)

    request_user_data = None

    for admin in admin_user_data:
        if RequestCircle.objects.filter(circle_id=admin.circle_id):
            if not request_user_data:
                request_user_data = list()
            request_user_data.extend(
                RequestCircle.objects.filter(circle_id=admin.circle_id))
    if request_user_data:
        requests = len(request_user_data)
    else:
        requests = 0

    return request_user_data, requests
