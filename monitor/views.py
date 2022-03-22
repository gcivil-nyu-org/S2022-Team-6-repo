from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .driver import get_s3_client, get_data
from circle.models import Circle, CircleUser, RequestCircle
from circle.helper import get_notifications


from django.core import signing


def base(request, user_enc):

    try:
        username = signing.loads(user_enc)
        response, client_object = get_s3_client()
        historical, live, average = get_data(client_object)
    except:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    context = {
        "page_name": "Monitor",
        "user_enc": user_enc,
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
    }
    return render(request, "monitor/index.html", context)
