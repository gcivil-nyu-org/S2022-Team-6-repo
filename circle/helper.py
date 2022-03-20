from .models import CircleUser, RequestCircle


def get_notifications(username, get_three=True):
    admin_user_data = CircleUser.objects.filter(username=username, is_admin=True)

    request_user_data = None

    for admin in admin_user_data:
        if RequestCircle.objects.filter(circle_id=admin.circle_id):
            if not request_user_data:
                request_user_data = list()
            request_user_data.extend(
                RequestCircle.objects.filter(circle_id=admin.circle_id)
            )
    if request_user_data:
        requests = len(request_user_data)
    else:
        requests = 0

    if get_three and request_user_data:
        if requests > 3:
            return request_user_data[:3], requests
        else:
            return request_user_data, requests
    else:
        return request_user_data, requests


def get_circle_requests(circle_id):
    return len(RequestCircle.objects.filter(circle_id=circle_id))
