from .models import (
    Circle,
    CircleUser,
    CirclePolicy,
    Policy,
    RequestCircle,
    RecentCircle,
    CirclePolicyCompliance,
)

from login.models import UserData, Privacy
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


def add_recent_circle(circle_data):
    recentcircle = RecentCircle.objects.get(username=circle_data.username)

    jsonDec = json.decoder.JSONDecoder()
    recent_circle_list = jsonDec.decode(recentcircle.recent_circle)

    if circle_data.circle_id.circle_id not in recent_circle_list:

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


def check_compliance(policy, username):
    policy_id = Policy.objects.get(policy_id=policy).policy_id

    if policy_id == 1:
        return Privacy.objects.get(username=username).show_vacination

    if policy_id == 2:
        return Privacy.objects.get(username=username).show_people_met

    if policy_id == 3:
        return Privacy.objects.get(username=username).show_location_visited


def create_circle(username, circle_name, policy_id, group_image):

    # Add Circle
    circle = Circle()
    circle.circle_name = circle_name
    circle.admin_username = UserData.objects.get(username=username)
    circle.save()

    if group_image:
        group_image.name = str(circle.circle_id) + "." + group_image.name.split(".")[-1]
        circle.group_image = group_image
        # circle.group_image.name = str(circle.circle_id)+ '.' + group_image.name.split('.')[-1]
        circle.save()

    # Add Admin user
    circleusers = CircleUser()
    circleusers.circle_id = Circle.objects.get(circle_id=circle.circle_id)
    circleusers.username = UserData.objects.get(username=username)
    circleusers.is_admin = True
    circleusers.save()

    for policy in policy_id:
        # Add Policy
        circlepolicy = CirclePolicy()
        circlepolicy.circle_id = Circle.objects.get(circle_id=circle.circle_id)
        circlepolicy.policy_id = Policy.objects.get(policy_id=int(policy))
        circlepolicy.save()

        # Add Policy Compliance
        policycomplicance = CirclePolicyCompliance()
        policycomplicance.circle_id = Circle.objects.get(circle_id=circle.circle_id)
        policycomplicance.policy_id = Policy.objects.get(policy_id=int(policy))
        policycomplicance.username = UserData.objects.get(username=username)
        policycomplicance.compliance = check_compliance(int(policy), username)
        policycomplicance.save()


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

    for current_policy in CirclePolicy.objects.filter(
        circle_id=current_request.circle_id.circle_id
    ):
        # Add Policy Compliance
        policy = current_policy.policy_id.policy_id
        policycomplicance = CirclePolicyCompliance()
        policycomplicance.circle_id = Circle.objects.get(
            circle_id=current_request.circle_id.circle_id
        )
        policycomplicance.policy_id = Policy.objects.get(policy_id=policy)
        policycomplicance.username = UserData.objects.get(
            username=current_request.username.username
        )
        policycomplicance.compliance = check_compliance(
            policy, current_request.username.username
        )
        policycomplicance.save()


def reject_request(request_id):
    temp = RequestCircle.objects.get(request_id=request_id)
    temp.delete()


def remove_user(admin_username, username, circle_id):

    # decrease number of users
    circle = Circle.objects.get(circle_id=circle_id)
    circle.no_of_users -= 1
    circle.save()

    # remove circleuser object
    circleusers = CircleUser.objects.get(circle_id=circle_id, username=username)
    circleusers.delete()

    # remove circlecompliance object
    policycomplicance = CirclePolicyCompliance.objects.filter(
        circle_id=circle_id, username=username
    )
    policycomplicance.delete()


def remove_circle(circle_id):
    circle = Circle.objects.get(circle_id=circle_id)
    circle.delete()
