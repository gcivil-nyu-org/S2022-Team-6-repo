from django.shortcuts import render

# from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .driver import get_s3_client, get_data

# from circle.models import CircleUser, Circle
from circle.helper import get_notifications


from django.core import signing
import math
import string

# import pandas as pd


def base(request):

    try:
        username = signing.loads(request.session["user_key"])
        response, client_object = get_s3_client()
        historical, live, average = get_data(client_object)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    # circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    df = historical[historical.county == "New York City"].copy(deep=True)

    df_2020 = df[(df.date < "2021-01-01") & (df.date >= "2020-08-01")].copy(deep=True)
    df_2021 = df[(df.date < "2022-01-01") & (df.date >= "2021-08-01")].copy(deep=True)

    # df_2020['date'] = pd.to_datetime(df_2020['date']).dt.date
    # df_2021['date'] = pd.to_datetime(df_2021['date']).dt.date
    # df_2020_1 = (df_2020[["date", "cases"]].values).tolist()
    df_2021_1 = (historical[["county", "cases"]].values).tolist()
    print(df_2021_1[0]," ", type(df_2021_1[0][0]))
    counties = []
    cases = []
    for i in range(len(df_2021_1)):
        if(type(df_2021_1[i][0]) is not str):
            #print("Inside Nan", df_2021_1[i][0])
            df_2021_1[i][0] = "Others"
        counties.append(df_2021_1[i][0])
        cases.append(df_2021_1[i][1])
        #if(math.isnan(float(df_2021_1[i][0]))):
    df_2020 = (df_2020[["date", "cases"]].values).tolist()
    df_2021 = (df_2021[["date", "cases"]].values).tolist()

    # print(df_2020)

    context = {
        "page_name": "Monitor",
        "username": username,
        "request_user_data": request_user_data,
        "requests": requests,
        "monitor": True,
        "df_2020": df_2020,
        "df_2021": df_2021,
        "df_2021_1": df_2021_1,
        "counties": counties,
        "cases": cases
    }
    return render(request, "monitor/index.html", context)
