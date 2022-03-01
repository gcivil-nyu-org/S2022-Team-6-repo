from django.shortcuts import render
from django.http import HttpResponse
from .models import Circle, CircleUser, CirclePolicy, Policy
# Create your views here.


def circle(request, username):
    circle_user_data = CircleUser.objects.filter(username=username)
    # print(circle_user_data[0].username.username)
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
        # 'circle_id': int(circleid),
        # 'username': username,
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
    return render(request, 'circle/add.html', context)
