from django.shortcuts import render
from .models import Selftrack


# Create your views here.


def selftrack(request, username):
    context = {"username": username}
    return render(request, "self_track.html", context)

def selftracksave(request, username):

    if request.method == "POST" and "signup-button" in request.POST:
        userdata = Selftrack()
        userdata.username = username
        userdata.usermet = request.POST.get("usermet")
        userdata.locationgone = request.POST.get("locationgone")
        userdata.save()

    return render(request, "self_track.html")