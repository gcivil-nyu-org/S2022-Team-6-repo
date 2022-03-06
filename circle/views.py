from django.shortcuts import render
from django.http import HttpResponse
from .models import Circle, CircleUser, CirclePolicy, Policy, RequestCircle
from login.models import UserData
from .helper import get_notifications


def circle(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Circle',
        'circle_user_data': circle_user_data,
        'username': username,
        'request_user_data': request_user_data[:3],
        'requests': requests
    }

    return render(request, 'circle/circle.html', context)


def current_circle(request, username, circleid):
    circle_data = CircleUser.objects.get(
        circle_id=circleid, username=username)

    circle_user_data = CircleUser.objects.filter(circle_id=circleid)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Circle Info',
        'circle_user_data': circle_user_data,
        'circle_data': circle_data,
        'request_user_data': request_user_data[:3],
        'requests': requests,
        'username': username
    }

    return render(request, 'circle/current-circle.html', context)


def create(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)

    circle = Circle.objects.filter(admin_username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Create',
        'circle_user_data': circle_user_data,
        'request_user_data': request_user_data[:3],
        'requests': requests,
        'username': username
    }

    if request.method == 'POST' and 'request_circle' in request.POST:
        requestcircle = RequestCircle()
        requestcircle.circle_id = Circle.objects.get(
            circle_id=request.POST.get('circle_id')
        )
        requestcircle.username = UserData.objects.get(
            username=username)
        requestcircle.save()

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

    return render(request, 'circle/add.html', context)


def notify(request, username):
    request_user_data, requests = get_notifications(username=username)

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
