# Django import
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing
from django.contrib import messages

# model import
from .models import SelfTrack
from login.models import UserData, Counties

# helper import
from circle.helper import get_notifications, get_all_non_compliance
from .helper import (
    check_date_uplaoded,
    check_uploaded_yesterday,
    get_current_streak,
    get_longest_streak,
    check_upload_today,
    get_all_connections,
)
from alert.helper import get_alert

# driver import
from .driver import add_user_met, add_location_visited

import datetime
import json


def selftrack(request, username):
    uploaded_today = False
    uploaded_yesterday = False
    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
        # _, client_object = get_s3_client()
        # historical, _, _ = get_data(client_object)
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
            selftrack.user_met = add_user_met(request.POST.getlist("user_met"))
            selftrack.location_visited = add_location_visited(
                request.POST.getlist("location_visited")
            )

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
            messages.success(request, "Great Job SelfTrack Successful!")
    else:

        if request.method == "POST" and "track-update" in request.POST:

            try:
                selftrack = SelfTrack.objects.filter(username=username).latest(
                    "date_uploaded"
                )
                selftrack.user_met = add_user_met(request.POST.getlist("user_met"))
                selftrack.location_visited = add_location_visited(
                    request.POST.getlist("location_visited")
                )
                selftrack.save()
                messages.success(request, "Updated Successfully!")

            except Exception:  # pragma: no cover
                messages.error(request, "Not able to update!")  # pragma: no cover

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    current_streak = get_current_streak(username)
    longest_streak = get_longest_streak(username)

    streak_today = check_upload_today(username)
    already_met = list()
    already_visited = list()

    if streak_today:
        jsonDec = json.decoder.JSONDecoder()

        selected = SelfTrack.objects.filter(username=username).latest("date_uploaded")

        already_visited = jsonDec.decode(selected.location_visited)
        already_met = jsonDec.decode(selected.user_met)

    streak_yesterday = check_uploaded_yesterday(username)
    alert = get_alert(username=username)

    connections = get_all_connections(username)

    counties = Counties.objects.all().values_list("county", flat=True)

    context = {
        "page_name": "SelfTrack",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # other
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "streak_yesterday": streak_yesterday,
        "selftrack": True,
        "counties": counties,
        "connections": connections,
        "already_visited": already_visited,
        "already_met": already_met,
    }
    return render(request, "selftracking/self_track.html", context)
