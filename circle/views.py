from django.shortcuts import render
from django.contrib import messages

from .models import Circle, CircleUser, RequestCircle
from .helper import get_notifications, get_circle_requests
from .driver import (
    create_request,
    create_circle,
    accept_request,
    reject_request,
    remove_user,
)
from django.core import signing


def circle(request, username):
    username1 = signing.loads(username)
    circle_user_data = CircleUser.objects.filter(username=username1)
    request_user_data, requests = get_notifications(username=username1)
    context = {
        "page_name": "Circle",
        "username": username1,
        "request_user_data": request_user_data,
        "requests": requests,
        # Other
        "circle_user_data": circle_user_data,
    }

    return render(request, "circle/circle.html", context)


def current_circle(request, username, circle_id):

    if request.method == "POST" and "remove_user" in request.POST:
        remove_user(username, request.POST.get("remove_user"), circle_id)

    circle_data = CircleUser.objects.get(circle_id=circle_id, username=username)

    circle_user_data = CircleUser.objects.filter(circle_id=circle_id)

    request_user_data, requests = get_notifications(username=username)

    if circle_data.is_admin:
        circle_request = get_circle_requests(circle_id)
    else:
        circle_request = None

    context = {
        "page_name": circle_data.circle_id.circle_name,
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
        # Other
        "circle_user_data": circle_user_data,
        "circle_data": circle_data,
        "circle_request": circle_request,
        "is_admin": circle_data.is_admin,
    }

    return render(request, "circle/current-circle.html", context)


def create(request, username):

    if request.method == "POST" and "request_circle" in request.POST:
        circle_id = request.POST.get("circle_id")
        try:
            Circle.objects.get(circle_id=circle_id)
            try:
                RequestCircle.objects.get(circle_id=circle_id, username=username)
                messages.error(request, "Request Pending!")
            except Exception as e:
                try:
                    CircleUser.objects.get(username=username, circle_id=circle_id)
                    messages.error(request, "Already a Member!", str(e))
                except Exception as e:
                    create_request(username, circle_id)
                    messages.success(request, "Request sent to Circle Admin", str(e))
        except Exception as e:
            messages.error(request, "Circle ID does not exist!", str(e))

    if request.method == "POST" and "create_circle" in request.POST:
        circle_name = request.POST.get("circle_name")

        counter = 0
        circleusers = CircleUser.objects.filter(username=username)

        for circleuser in circleusers:
            if circleuser.circle_id.circle_name == circle_name:
                counter += 1

        try:
            if counter > 0:
                raise Exception("Circle Name already Exist - Adding Counter to end!!")

            create_circle(username, circle_name, request.POST.getlist("policy_id"))
        except Exception as e:
            messages.error(request, str(e))

            create_circle(
                username,
                circle_name + "(" + str(counter) + ")",
                request.POST.getlist("policy_id"),
            )

    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        "page_name": "Add Circle",
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
        # Other
        "circle_user_data": circle_user_data,
    }

    return render(request, "circle/add.html", context)


def notify(request, username):

    if request.method == "POST" and "accept_circle" in request.POST:
        accept_request(request.POST.get("accept_circle"))

    if request.method == "POST" and "reject_circle" in request.POST:
        reject_request(request.POST.get("reject_circle"))

    request_user_data, requests = get_notifications(username=username, get_three=False)

    context = {
        "page_name": "Notifications",
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests
        # Other
    }

    return render(request, "circle/notifications.html", context)
