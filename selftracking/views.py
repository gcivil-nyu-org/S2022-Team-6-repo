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
)


def selftrack(request, username):
    uploaded_today = False
    new_user = False
    uploaded_yesterday = False
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

    if (not uploaded_yesterday and not new_user) and not check_date_uplaoded(
        username, default=False
    ):
        selftrack = SelfTrack()
        selftrack.username = UserData.objects.get(username=username)
        selftrack.user_met = "42a7b2626eae970122e01f65af2f5092"
        selftrack.location_visited = "42a7b2626eae970122e01f65af2f5092"
        selftrack.streak = 0

        if get_current_streak(username) > get_longest_streak(username):
            selftrack.largest_streak = get_current_streak(username)
        else:
            selftrack.largest_streak = get_longest_streak(username)

        selftrack.save()

    if new_user or not uploaded_today:

        if request.method == "POST" and "track" in request.POST:
            selftrack = SelfTrack()
            selftrack.username = UserData.objects.get(username=username)
            selftrack.user_met = request.POST.get("user_met")
            selftrack.location_visited = request.POST.get("user_met")

            if not new_user:
                selftrack.streak = get_current_streak(username) + 1

                if get_current_streak(username) > get_longest_streak(username):
                    selftrack.largest_streak = get_current_streak(username)
                else:
                    selftrack.largest_streak = get_longest_streak(username)

            else:
                selftrack.streak = 1
                selftrack.largest_streak = 1

            selftrack.save()
            uploaded_today = True
            new_user = False

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    if not new_user:
        current_streak = get_current_streak(username)
    else:
        current_streak = 0

    context = {
        "page_name": "SelfTrack",
        "username": username,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        # other
        "uploaded_today": uploaded_today,
        "current_streak": current_streak,
        "new_user": new_user,
    }
    return render(request, "selftracking/self_track.html", context)
