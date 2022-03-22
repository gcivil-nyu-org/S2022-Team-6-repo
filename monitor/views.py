from django.shortcuts import render
from django.contrib import messages
from coviguard.s3_config import s3Config


def base(request, username):
    context = {
        username: username
    }
    return render(request, "monitor/index.html", context)
