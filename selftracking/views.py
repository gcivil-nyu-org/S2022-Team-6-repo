from django.shortcuts import render
from .models import SelfTrack
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing
from login.models import UserData
from circle.helper import get_notifications

from .helper import (
    check_date_uplaoded,
    check_uploaded_yesterday,
    get_current_streak,
)


def selftrack(request, username):
    uploaded_today = False
    new_user = False
    try:
        username = signing.loads(request.session["user_key"])
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    try:
        uploaded_today = check_date_uplaoded(username)
        uploaded_yesterday = check_uploaded_yesterday(username)
    except Exception:
        new_user = True

    if new_user or not uploaded_today:

        if request.method == "POST" and "track" in request.POST:
            selftrack = SelfTrack()
            selftrack.username = UserData.objects.get(username=username)
            selftrack.user_met = request.POST.get("user_met")
            selftrack.location_visited = request.POST.get("user_met")

            if not new_user:
                if uploaded_yesterday:
                    selftrack.streak = get_current_streak(username) + 1
                else:
                    selftrack.streak = 0

                    longest_streak = get_current_streak(username)
                    selftrack.largest_streak = longest_streak
            else:
                selftrack.streak = 1

            selftrack.save()
            uploaded_today = True
            new_user = False

    request_user_data, requests = get_notifications(username=username)

    if not new_user:
        current_streak = get_current_streak(username)
    else:
        current_streak = 0

    context = {
        "page_name": "SelfTrack",
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
        # other
        "uploaded_today": uploaded_today,
        "current_streak": current_streak,
        "new_user": new_user,
    }
    return render(request, "selftracking/self_track.html", context)
