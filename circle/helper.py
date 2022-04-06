from .models import (
    Circle,
    CircleUser,
    RequestCircle,
    CirclePolicyCompliance,
    RecentCircle,
)
from login.models import UserData

import json


def get_circle_compliance(circle_id):
    compliance_dict = dict()

    circle_compliance = CirclePolicyCompliance.objects.filter(circle_id=circle_id)

    for compliance in circle_compliance:
        if compliance.username.username not in compliance_dict.keys():
            compliance_dict[compliance.username.username] = dict()
        if compliance.compliance:
            compliance_dict[compliance.username.username][
                compliance.policy_id.policy_id
            ] = "Compliant"
        else:
            compliance_dict[compliance.username.username][
                compliance.policy_id.policy_id
            ] = "Not Compliant"

    return compliance_dict


def get_all_non_compliance(username, get_three):

    circle_compliance = CirclePolicyCompliance.objects.filter(username=username)

    non_compliance = None

    for compliance in circle_compliance:
        if not compliance.compliance:
            if not non_compliance:
                non_compliance = list()
            non_compliance.append(compliance)

    if non_compliance and get_three:
        if len(non_compliance) > 3:
            return non_compliance[:3], len(non_compliance)

    if not non_compliance:
        return non_compliance, 0
    else:
        return non_compliance, len(non_compliance)


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


def get_recent_circles(recent_circle_list, username):  # TODO: Recent Circle

    recent_circles = list()

    for circle in recent_circle_list:
        recent_circles.append(
            CircleUser.objects.get(circle_id=circle, username=username)
        )

    return recent_circles


def check_recent_circle(recent_circle_list, username):

    for recent_circle in recent_circle_list:
        try:
            CircleUser.objects.get(
                username=UserData.objects.get(username=username),
                circle_id=Circle.objects.get(circle_id=recent_circle),
            )
        except Exception:
            remove_recent_circle(recent_circle, username)

    return recent_circle_list


def remove_recent_circle(circle_id, username):
    recentcircle = RecentCircle.objects.get(username=username)

    jsonDec = json.decoder.JSONDecoder()
    recent_circle_list = jsonDec.decode(recentcircle.recent_circle)

    recent_circle_list.remove(circle_id)

    recentcircle.recent_circle = json.dumps(recent_circle_list)
    recentcircle.save()

    return recent_circle_list


# def get_recent_circles(request, username):
#     if 'recent_circle' in request.sessions.keys():
#         return request.session['recent_circle']
#     else:
#         return list()
