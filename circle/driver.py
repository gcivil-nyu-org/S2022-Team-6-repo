from .models import (
    Circle,
    CircleUser,
    CirclePolicy,
    Policy,
    RequestCircle,
    RecentCircle,
)
from login.models import UserData
import json


def recent_circle(username):
    user_data = UserData.objects.get(username=username)

    recent_circle_list = list()

    if len(RecentCircle.objects.filter(username=user_data)) == 0:

        recentcircle = RecentCircle()
        recentcircle.username = user_data
        recentcircle.recent_circle = json.dumps([])
        recentcircle.save()

    else:
        recentcircle = RecentCircle.objects.get(username=user_data)

        jsonDec = json.decoder.JSONDecoder()
        recent_circle_list = jsonDec.decode(recentcircle.recent_circle)

    return recent_circle_list


def get_recent_circles(recent_circle_list, username):

    recent_circles = list()

    for circle in recent_circle_list:
        recent_circles.append(
            CircleUser.objects.get(circle_id=circle, username=username)
        )

    return recent_circles


def add_recent_circle(circle_data):
    recentcircle = RecentCircle.objects.get(username=circle_data.username)

    jsonDec = json.decoder.JSONDecoder()
    recent_circle_list = jsonDec.decode(recentcircle.recent_circle)

    if not circle_data.circle_id.circle_id in recent_circle_list:

        if len(recent_circle_list) == 3:
            recent_circle_list.pop(0)
            recent_circle_list.append(circle_data.circle_id.circle_id)
        else:
            recent_circle_list.append(circle_data.circle_id.circle_id)

        recentcircle.recent_circle = json.dumps(recent_circle_list)

        recentcircle.save()


def create_request(username, circle_id):

    requestcircle = RequestCircle()
    requestcircle.circle_id = Circle.objects.get(circle_id=circle_id)
    requestcircle.username = UserData.objects.get(username=username)
    requestcircle.save()


def create_circle(username, circle_name, policy_id):

    circle = Circle()

    circle.circle_name = circle_name
    circle.admin_username = UserData.objects.get(username=username)
    circle.save()

    circleusers = CircleUser()
    circleusers.circle_id = Circle.objects.get(circle_id=circle.circle_id)
    circleusers.username = UserData.objects.get(username=username)
    circleusers.is_admin = True
    circleusers.save()

    for policy in policy_id:
        circlepolicy = CirclePolicy()
        circlepolicy.circle_id = Circle.objects.get(circle_id=circle.circle_id)
        circlepolicy.policy_id = Policy.objects.get(policy_id=int(policy))
        circlepolicy.save()


def accept_request(request_id):

    current_request = RequestCircle.objects.get(request_id=request_id)

    circleusers = CircleUser()

    circleusers.circle_id = Circle.objects.get(
        circle_id=current_request.circle_id.circle_id
    )

    circleusers.username = UserData.objects.get(
        username=current_request.username.username
    )
    circleusers.is_admin = False
    circleusers.is_member = True

    circle = Circle.objects.get(circle_id=current_request.circle_id.circle_id)
    circle.no_of_users += 1

    circle.save()
    circleusers.save()
    current_request.delete()


def reject_request(request_id):
    temp = RequestCircle.objects.get(request_id=request_id)
    temp.delete()


def remove_user(admin_username, username, circle_id):

    circle = Circle.objects.get(circle_id=circle_id)
    circle.no_of_users -= 1
    circle.save()

    circleusers = CircleUser.objects.get(circle_id=circle_id, username=username)

    circleusers.delete()


def remove_circle(circle_id):
    circle = Circle.objects.get(circle_id=circle_id)
    circle.delete()
