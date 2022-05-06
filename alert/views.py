# Django Alerts
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import signing
from django.core.paginator import Paginator

# Model imports
from login.models import UserData
from alert.models import AlertNotification

# Helper imports
from circle.helper import get_notifications, get_all_non_compliance
from selftracking.helper import (
    check_upload_today,
    get_current_streak,
    check_uploaded_yesterday,
)
from .helper import get_alert

# Global Variable
ALERT_PER_PAGE = 10


# Create your views here.
def alert_user(request, username):
    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)  # pragma: no cover
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "read-button" in request.POST:
        for id in request.POST.getlist("id"):
            read_alert = AlertNotification.objects.get(id=id)
            read_alert.read = True
            read_alert.save()

    alert_notifications = AlertNotification.objects.filter(
        username=username
    ).order_by(  # pragma: no cover
        "-updated"  # pragma: no cover
    )

    if len(alert_notifications) > 0:
        alerts_available = True  # pragma: no cover
    else:
        alerts_available = False

    paginator = Paginator(alert_notifications, ALERT_PER_PAGE)
    page = request.GET.get("page")
    alert_notification = paginator.get_page(page)

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)
    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    streak_yesterday = check_uploaded_yesterday(username)
    alert = get_alert(username=username)
    current_streak = get_current_streak(username)

    context = {
        "page_name": "Alert",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        "current_streak": current_streak,
        "streak_yesterday": streak_yesterday,
        # other
        "alert_notification": alert_notification,
        "alerts_available": alerts_available,
    }

    return render(request, "alert/alert.html", context)


def markAllAsRead(request, username):
    try:
        username = signing.loads(request.session["user_key"])
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)
    AlertNotification.objects.filter(username=username).update(read=True)
    return alert_user(request, username)
