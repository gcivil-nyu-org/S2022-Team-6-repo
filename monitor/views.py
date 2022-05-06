from django.shortcuts import render

# from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .driver import get_s3_client, get_data

# from circle.models import CircleUser, Circle
from circle.helper import get_notifications, get_all_non_compliance


from django.core import signing

# import pandas as pdcondaavtivate
from .helper import convert_datetime
from selftracking.helper import (
    check_upload_today,
    get_current_streak,
    check_uploaded_yesterday,
)

from alert.helper import get_alert

from login.models import UserData
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def base(request):

    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
        _, client_object = get_s3_client()
        historical, _, _ = get_data(client_object)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    currentTimeDate = date.today() - relativedelta(years=1)
    currentTimeDate = (currentTimeDate.replace(day=1) + timedelta(days=32)).replace(
        day=1
    )
    currentTimeDate = "20" + currentTimeDate.strftime("%y-%m-%d")
    df = historical[(historical.date >= currentTimeDate)]

    historical = historical[historical.state == "New York"]

    df = df[df.state == "New York"]
    df_2021_all = (df[["date", "cases", "county"]].values).tolist()

    df_2021 = df[df.county == "New York City"]
    df_2021 = (df_2021[["date", "cases"]].values).tolist()
    categories = [convert_datetime(df_2021[i][0]) for i in range(0, 153)]

    home_location = userdata.home_adress  # pragma: no cover
    work_location = userdata.work_address  # pragma: no cover
    # if home_location is None or len(home_location) == 0:
    #     home_location = "New York City"
    # if work_location is None or len(work_location) == 0:
    #     work_location = "New York City"

    df_2021_home = (df[df.county == home_location][["date", "cases"]].values).tolist()
    df_2021_work = (df[df.county == work_location][["date", "cases"]].values).tolist()

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    current_streak = get_current_streak(username)
    streak_yesterday = check_uploaded_yesterday(username)
    counties = historical
    counties = counties.county.dropna().unique()
    counties = counties[counties != "Unknown"]

    historical = (historical[["date", "cases", "county"]].values).tolist()

    context = {
        "page_name": "Monitor",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "current_streak": current_streak,
        "monitor": True,
        "alert": alert,
        "df_2021": df_2021,
        "categories_2021": categories,
        "df_2021_home": df_2021_home,
        "df_2021_work": df_2021_work,
        "locations": [home_location, work_location],
        "counties": counties,
        "df_2021_all": df_2021_all,
        "historical": historical,
        "home_location": home_location,
        "work_location": work_location,
        "streak_yesterday": streak_yesterday,
    }
    return render(request, "monitor/index.html", context)
