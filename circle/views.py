from django.shortcuts import render
from django.http import HttpResponse
from .models import Circle, CircleUser, CirclePolicy, Policy, RequestCircle
from login.models import UserData
from .helper import get_notifications, get_circle_requests


def circle(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Circle',
        'circle_user_data': circle_user_data,
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests
    }

    return render(request, 'circle/circle.html', context)


def current_circle(request, username, circle_id):
    circle_data = CircleUser.objects.get(
        circle_id=circle_id, username=username)

    circle_user_data = CircleUser.objects.filter(circle_id=circle_id)

    request_user_data, requests = get_notifications(username=username)

    is_admin = False

    if circle_data.is_admin:
        circle_request = get_circle_requests(circle_id)
        is_admin = True
    else:
        circle_request = None

    context = {
        'page_name': 'Circle Info',
        'circle_user_data': circle_user_data,
        'circle_data': circle_data,
        'request_user_data': request_user_data,
        'requests': requests,
        'circle_request': circle_request,
        'username': username,
        'is_admin': circle_data.is_admin
    }

    return render(request, 'circle/current-circle.html', context)


def create(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)

    circle = Circle.objects.filter(admin_username=username)

    request_user_data, requests = get_notifications(username=username)

    if request.method == 'POST' and 'request_circle' in request.POST:

        try:
            CircleUser.objects.get(
                username=username, circle_id=request.POST.get('circle_id'))
            already_member = True
        except:
            already_member = False

        if not already_member:
            requestcircle = RequestCircle()
            requestcircle.circle_id = Circle.objects.get(
                circle_id=request.POST.get('circle_id')
            )
            requestcircle.username = UserData.objects.get(
                username=username)
            requestcircle.save()

    # TODO: Already member alert

    if request.method == 'POST' and 'create_circle' in request.POST:
        circle = Circle()
        circleusers = CircleUser()
        circle.circle_name = request.POST.get('circle_name')
        circle.admin_username = UserData.objects.get(
            username=username)
        circle.save()
        circleusers.circle_id = Circle.objects.get(
            circle_id=circle.circle_id
        )
        circleusers.username = UserData.objects.get(
            username=username)
        circleusers.is_admin = True
        circleusers.save()
        for policy in request.POST.getlist('policy_id'):
            circlepolicy = CirclePolicy()
            circlepolicy.circle_id = Circle.objects.get(
                circle_id=circle.circle_id
            )
            circlepolicy.policy_id = Policy.objects.get(
                policy_id=int(policy)
            )
            circlepolicy.save()

    context = {
        'page_name': 'Create',
        'circle_user_data': circle_user_data,
        'request_user_data': request_user_data,
        'requests': requests,
        'username': username
    }

    return render(request, 'circle/add.html', context)


def notify(request, username):
    request_user_data, requests = get_notifications(
        username=username, get_three=False)

    if request.method == 'POST' and 'accept_circle' in request.POST:
        circleusers = CircleUser()
        current_request = RequestCircle.objects.get(request_id=request.POST.get(
            'accept_circle'
        ))

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

    if request.method == 'POST' and 'reject_circle' in request.POST:
        temp = RequestCircle.objects.get(request_id=request.POST.get(
            'reject_circle'
        ))
        temp.delete()

    context = {
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests
    }

    return render(request, 'circle/notifications.html', context)
    return render(request, 'circle/add.html', context)


def remove_user(request, circleid, username):
    adminuser = Circle.objects.get(circle_id=circleid)
    if (adminuser.admin_username.username != username):
        circle_data = CircleUser.objects.filter(
            circle_id=circleid, username=username)
        circle_data.delete()
        adminuser.no_of_users -= 1
        adminuser.save()
    circle_data = CircleUser.objects.get(
        circle_id=circleid, username=adminuser.admin_username.username)
    circle_user_data = CircleUser.objects.filter(circle_id=circleid)
    circle = Circle.objects.get(circle_id=circleid)
    context = {
        'page_name': 'Circle Info',
        'circle_user_data': circle_user_data,
        'circle_data': circle_data,
        'isAdmin': True
    }
    return render(request, 'circle/current-circle.html', context)
