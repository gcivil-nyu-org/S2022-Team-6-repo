from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import UserData
from circle.models import CircleUser
from django.core.signing import TimestampSigner
from django.core import signing


# Create your views here.


def index(request):
    context = {"page_name": "CoviGuard", "css_name": "login"}
    return render(request, "login/index.html", context)


def signin(request):
    context = {"page_name": "SignIn"}

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
        url = reverse("circle", kwargs={"username": userEnc})
        return HttpResponseRedirect(url)

    return render(request, "login/signup.html", context)


def login(request):
    email_id = request.POST.get("email")
    password = request.POST.get("password")
    print(email_id)
    if UserData.objects.filter(email=email_id).first():
        user = UserData.objects.get(email=email_id)
        username1 = user.username
        userEnc = signing.dumps(username1)
        if user.password == password:
            url = reverse("circle", kwargs={"username": userEnc})
            return HttpResponseRedirect(url)

        else:
            return HttpResponse("Incorrect Password")
    else:
        return HttpResponse("No User Found or Incorrect password")
