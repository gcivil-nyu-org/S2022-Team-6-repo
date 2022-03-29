from django.shortcuts import render
from .models import SelfTrack
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing
from login.models import UserData
from circle.helper import get_notifications


def selftrack(request, username):
    try:
        username = signing.loads(request.session["user_key"])
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "track" in request.POST:
        userdata = SelfTrack()
        userdata.username = UserData.objects.get(username=username)
        userdata.user_met = request.POST.get("usermet")
        userdata.location_visited = request.POST.get("locationgone")
        userdata.save()

    request_user_data, requests = get_notifications(username=username)

    context = {
        "page_name": "SelfTrack",
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
    }
    return render(request, "selftracking/self_track.html", context)
