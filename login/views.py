from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core import signing

from .models import UserData

# CURRENT_SESSION_VALID = False


def profile(request, username):
    try:
        current_username = signing.loads(request.session["user_key"])
        if not current_username == username:
            print("error")
            raise Exception()
    except Exception:
        try:
            userdata = UserData.objects.get(username=username)
            context = {
                "page_name": username,
                "session_valid": False,
            }
            return render(request, "login/profile.html", context)
        except Exception:
            url = reverse("login:error")
            return HttpResponseRedirect(url)

    userdata = UserData.objects.get(username=current_username)

    context = {
        "page_name": current_username,
        "session_valid": True,
        "username": username,
    }

    return render(request, "login/user_profile.html", context)


def index(request):
    current_session_valid = False
    if "user_key" in request.session.keys():
        current_session_valid = True
        username = signing.loads(request.session["user_key"])
    if current_session_valid:
        context = {
            "page_name": "CoviGuard",
            "css_name": "login",
            "session_valid": current_session_valid,
            "username": username,
        }
    else:
        context = {
            "page_name": "CoviGuard",
            "css_name": "login",
            "session_valid": current_session_valid,
        }
    return render(request, "login/index.html", context)


def signin(request):
    if request.method == "POST" and "sign-in" in request.POST:
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = UserData.objects.get(username=username)

            user_enc = signing.dumps(username)
            request.session["user_key"] = user_enc
            if user.password == password:
                url = reverse("circle:dashboard", kwargs={"username": username})
                return HttpResponseRedirect(url)
            else:
                raise Exception("Invalid Password")
        except Exception:
            messages.error(request, "Invalid Username or Password")

    context = {"page_name": "Sign in"}
    return render(request, "login/signin.html", context)


def signup(request):

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
