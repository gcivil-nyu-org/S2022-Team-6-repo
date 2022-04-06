from django.shortcuts import render
from .models import SelfTrack
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing
from login.models import UserData
from circle.helper import get_notifications, get_all_non_compliance

from .helper import (
    check_date_uplaoded,
    check_uploaded_yesterday,
    get_current_streak,
    get_longest_streak,
    check_upload_today,
)

import datetime


def selftrack(request, username):
    uploaded_today = False
    uploaded_yesterday = False
    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    try:
        if len(SelfTrack.objects.filter(username=username)) == 0:
            raise Exception()
    except Exception:
        # if new user
        selftrack = SelfTrack()
        selftrack.username = UserData.objects.get(username=username)
        selftrack.user_met = "42a7b2626eae970122e01f65af2f5092"
        selftrack.location_visited = "42a7b2626eae970122e01f65af2f5092"
        selftrack.date_uploaded = datetime.date.today() + datetime.timedelta(days=-1)
        selftrack.streak = 0
        selftrack.largest_streak = 0
        selftrack.save()

    uploaded_today = check_date_uplaoded(username)

    if not uploaded_today:

        if request.method == "POST" and "track" in request.POST:
            selftrack = SelfTrack()
            selftrack.username = UserData.objects.get(username=username)
            selftrack.user_met = request.POST.get("user_met")
            selftrack.location_visited = request.POST.get("location_visited")

            uploaded_yesterday = check_uploaded_yesterday(username)

            if uploaded_yesterday:
                selftrack.streak = get_current_streak(username) + 1
            else:
                selftrack.streak = 1

            if selftrack.streak > get_longest_streak(username):
                selftrack.largest_streak = selftrack.streak
            else:
                selftrack.largest_streak = get_longest_streak(username)

            selftrack.save()

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    current_streak = get_current_streak(username)
    longest_streak = get_longest_streak(username)

    streak_today = check_upload_today(username)
    context = {
        "page_name": "SelfTrack",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        # other
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    }
    return render(request, "selftracking/self_track.html", context)
