from django.shortcuts import render
from django.http import HttpResponse
from .models import Circle, CircleUser, CirclePolicy, Policy, RequestCircle
from login.models import UserData
from .helper import *
from .driver import *


def circle(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Circle',
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests,
        # Other
        'circle_user_data': circle_user_data,
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
        'page_name': circle_data.circle_id.circle_name,
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests,
        # Other
        'circle_user_data': circle_user_data,
        'circle_data': circle_data,
        'circle_request': circle_request,
        'is_admin': circle_data.is_admin
    }

    return render(request, 'circle/current-circle.html', context)


def create(request, username):

    if request.method == 'POST' and 'request_circle' in request.POST:
        create_request(username, request.POST.get('circle_id'))
        # TODO: Already member alert

    if request.method == 'POST' and 'create_circle' in request.POST:
        create_circle(username, request.POST.get('circle_name'),
                      request.POST.getlist('policy_id'))

    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        'page_name': 'Add Circle',
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests,
        # Other
        'circle_user_data': circle_user_data
    }

    return render(request, 'circle/add.html', context)


def notify(request, username):

    if request.method == 'POST' and 'accept_circle' in request.POST:
        accept_request(request.POST.get(
            'accept_circle'))

    if request.method == 'POST' and 'reject_circle' in request.POST:
        reject_request(request.POST.get(
            'reject_circle'))

    request_user_data, requests = get_notifications(
        username=username, get_three=False)

    context = {
        'page_name': 'Notifications',
        'username': username,
        'request_user_data': request_user_data,
        'requests': requests
        # Other
    }

    return render(request, 'circle/notifications.html', context)


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
