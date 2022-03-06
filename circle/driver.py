from .models import Circle, CircleUser, CirclePolicy, Policy, RequestCircle
from login.models import UserData


def create_request(username, circle_id):

    try:
        CircleUser.objects.get(
            username=username, circle_id=request.POST.get('circle_id'))
        already_member = True
    except:
        already_member = False

    if not already_member:
        requestcircle = RequestCircle()
        requestcircle.circle_id = Circle.objects.get(
            circle_id=circle_id
        )
        requestcircle.username = UserData.objects.get(
            username=username)
        requestcircle.save()

    return already_member


def create_circle(username, circle_name, policy_id):

    circle = Circle()

    circle.circle_name = circle_name
    circle.admin_username = UserData.objects.get(
        username=username)
    circle.save()

    circleusers = CircleUser()
    circleusers.circle_id = Circle.objects.get(
        circle_id=circle.circle_id
    )
    circleusers.username = UserData.objects.get(
        username=username)
    circleusers.is_admin = True
    circleusers.save()

    for policy in policy_id:
        circlepolicy = CirclePolicy()
        circlepolicy.circle_id = Circle.objects.get(
            circle_id=circle.circle_id
        )
        circlepolicy.policy_id = Policy.objects.get(
            policy_id=int(policy)
        )
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

    circle = Circle.objects.get(
        circle_id=current_request.circle_id.circle_id
    )
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

    circleusers = CircleUser.objects.get(
        circle_id=circle_id, username=username)

    circleusers.delete()
