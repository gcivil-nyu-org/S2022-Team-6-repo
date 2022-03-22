from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core import signing

from .models import UserData


def index(request):
    context = {"page_name": "CoviGuard", "css_name": "login"}
    return render(request, "login/index.html", context)


def signin(request):
    if request.method == "POST" and "sign-in" in request.POST:
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = UserData.objects.get(username=username)

            user_enc = signing.dumps(username)

            if user.password == password:
                url = reverse("circle:dashboard", kwargs={"user_enc": user_enc})
                return HttpResponseRedirect(url)
            else:
                raise Exception("Invalid Password")
        except Exception as e:
            messages.error(request, "Invalid Username or Password")

    context = {"page_name": "Sign in"}
    return render(request, "login/signin.html", context)


def signup(request):
    context = {"page_name": "SignUp"}

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

        user = UserData.objects.get(username=userdata.username)
        username1 = user.username
        userEnc = signing.dumps(username1)
        url = reverse("circle:dashboard", kwargs={"username": userEnc})
        return HttpResponseRedirect(url)

    return render(request, "login/signup.html", context)


def error(request):
    return render(request, "login/error.html")
