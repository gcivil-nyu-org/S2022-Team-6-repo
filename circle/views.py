from django.shortcuts import render
from django.http import HttpResponse
from .models import Circle, CircleUser, CirclePolicy, Policy
from login.models import UserData


def circle(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)
    print(circle_user_data)
    context = {
        'page_name': 'Circle',
        'circle_user_data': circle_user_data,
        'username': username
    }
    return render(request, 'circle/circle.html', context)


def current_circle(request, username, circleid):
    circle_data = CircleUser.objects.get(
        circle_id=circleid, username=username)
    circle_user_data = CircleUser.objects.filter(circle_id=circleid)
    print(type(circle_user_data))
    context = {
        'page_name': 'Circle Info',
        'circle_user_data': circle_user_data,
        'circle_data': circle_data
    }
    return render(request, 'circle/current-circle.html', context)


def create(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)
    context = {
        'page_name': 'Create',
        'circle_user_data': circle_user_data
    }
    if request.method == 'POST' and 'request_circle' in request.POST:
        print(request.POST.get('circle_id'))
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
