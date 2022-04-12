# from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing

from login.models import UserData

from circle.helper import get_notifications, get_all_non_compliance
from selftracking.helper import check_upload_today


# Create your views here.
def alert_user(request, username):
    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)
    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)

    context = {
        "page_name": "Alert",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
    }

    return render(request, "alert/alert.html", context)
