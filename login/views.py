from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core import signing

from .models import UserData

# CURRENT_SESSION_VALID = False


def index(request):
    current_session_valid = False
    if "user_key" in request.session.keys():
        current_session_valid = True

    context = {
        "page_name": "CoviGuard",
        "css_name": "login",
        "session_valid": current_session_valid,
    }
    return render(request, "login/index.html", context)


def signin(request):

    # if "user_key" in request.session.keys():
    #     CURRENT_SESSION_VALID = True

    if request.method == "POST" and "sign-in" in request.POST:
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = UserData.objects.get(username=username)

            user_enc = signing.dumps(username)
            request.session["user_key"] = user_enc
            if user.password == password:
                url = reverse("circle:dashboard")
                return HttpResponseRedirect(url)
            else:
                raise Exception("Invalid Password")
        except Exception:
            messages.error(request, "Invalid Username or Password")

    context = {"page_name": "Sign in"}
    return render(request, "login/signin.html", context)


def signup(request):

    # if "user_key" in request.session.keys():
    #     CURRENT_SESSION_VALID = True

    try:
        if request.method == "POST" and "signup-button" in request.POST:
            userdata = UserData()
            userdata.firstname = request.POST.get("firstname")
            userdata.lastname = request.POST.get("lastname")
            userdata.username = request.POST.get("username")
            userdata.password = request.POST.get("password")
            userdata.email = request.POST.get("email")
            userdata.dob = request.POST.get("DoB")
            userdata.phone = request.POST.get("phonenumber")
            userdata.work_address = request.POST.get("ZipWork")
            userdata.home_adress = request.POST.get("ZipHome")
            is_vaxxed = False
            if request.POST.get("vaccination") == 1:
                is_vaxxed = True
            userdata.is_vacinated = is_vaxxed
            userdata.save()

            return HttpResponseRedirect(reverse("login:signin"))
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    context = {"page_name": "SignUp"}
    return render(request, "login/signup.html", context)


def logout(request):
    del request.session["user_key"]

    return HttpResponseRedirect(reverse("login:index"))


def error(request):
    return render(request, "login/error.html")
