# Django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core import signing

# other
from .hashes import PBKDF2WrappedSHA1PasswordHasher

# models
from .models import UserData, Privacy, Counties
from circle.models import CircleUser
from .helper import update_compliance
from alert.models import Alert

# helper
from selftracking.helper import (
    check_upload_today,
    get_current_streak,
    check_uploaded_yesterday,
)
from alert.helper import get_alert
from circle.helper import get_notifications, get_all_non_compliance

# # driver
# from monitor.driver import get_s3_client, get_data


def profile_view(request, username):
    try:
        view_userdata = UserData.objects.get(username=username)
    except Exception:
        # invlaid user url #
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    view_circles = CircleUser.objects.filter(username=view_userdata.username)

    try:
        # check user logged in
        current_username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=current_username)

        if current_username == username:
            return user_profile(request, username)

    except Exception:

        context = {
            "page_name": username,
            "username": username,
            # other
            "view_userdata": view_userdata,
            "session_valid": False,
            "circles": view_circles,
        }

        return render(request, "login/profile-general.html", context)

    logged_circles = CircleUser.objects.filter(username=userdata.username)

    common_circles = logged_circles.values("circle_id").intersection(
        view_circles.values("circle_id")
    )
    other_circles = view_circles.values("circle_id").difference(common_circles)

    common_circles = CircleUser.objects.filter(
        username=view_userdata.username, circle_id__in=common_circles
    )
    other_circles = CircleUser.objects.filter(
        username=view_userdata.username, circle_id__in=other_circles
    )

    # print(view_circles.values("circle_id"))
    # print(logged_circles.values("circle_id"))
    # print(CircleUser.objects.filter(username=view_userdata.username, circle_id__in=common_circles))
    # print(other_circles)
    # common_circles = list()
    # other_circles = list()

    # for circle_views in view_circles:
    #     for circle_logged in logged_circles:
    #         if circle_views.circle_id.circle_id == circle_logged.circle_id.circle_id:
    #             common_circles.append()

    request_user_data, requests = get_notifications(username=userdata.username)
    three_non_compliance, non_compliance = get_all_non_compliance(
        userdata.username, True
    )

    total_notify = requests + non_compliance
    streak_today = check_upload_today(userdata.username)
    alert = get_alert(username=userdata.username)

    current_streak = get_current_streak(userdata.username)
    streak_yesterday = check_uploaded_yesterday(userdata.username)

    context = {
        "page_name": username,
        "username": current_username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        "current_streak": current_streak,
        "streak_yesterday": streak_yesterday,
        # other
        "view_userdata": view_userdata,
        "session_valid": True,
        "common_circles": common_circles,
        "other_circles": other_circles,
    }
    # valid username
    return render(request, "login/profile-login.html", context)


def user_profile(request, username):
    try:
        # check valid username
        userdata = UserData.objects.get(username=username)
        # _, client_object = get_s3_client()
        # historical, _, _ = get_data(client_object)
    except Exception:
        # not a valid username
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    # valid username
    try:
        # check user logged in
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
    except Exception:
        # user not logged in
        url = reverse("login:profile", kwargs={"username": username})
        return HttpResponseRedirect(url)

    if request.method == "POST" and "submit_change" in request.POST:
        try:
            userdata = UserData.objects.get(username=username)

            if "first_name" in request.POST:
                userdata.firstname = request.POST["first_name"]

            if "last_name" in request.POST:
                userdata.lastname = request.POST["last_name"]

            if "dob" in request.POST and request.POST["dob"]:
                userdata.dob = request.POST["dob"]

            if "phone" in request.POST:
                userdata.phone = request.POST["phone"]

            if "home" in request.POST:
                userdata.home_adress = request.POST["home"]

            if "work" in request.POST:
                userdata.work_address = request.POST["work"]

            if "vaccination_status_yes" in request.POST:
                userdata.is_vacinated = True

            if "vaccination_status_no" in request.POST:
                userdata.is_vacinated = False

            if request.FILES:
                user_image = request.FILES["user_image"]
                user_image.name = (
                    userdata.username + "." + user_image.name.split(".")[-1]
                )
                userdata.user_image = user_image

            userdata.save()
        except Exception:
            messages.error(request, "Invalid Field")

    # user logged in
    userdata = UserData.objects.get(username=username)

    counties = Counties.objects.all().values_list("county", flat=True)

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    current_streak = get_current_streak(userdata.username)
    streak_yesterday = check_uploaded_yesterday(username)

    context = {
        "page_name": username,
        "username": current_username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        "current_streak": current_streak,
        "streak_yesterday": streak_yesterday,
        # other
        "counties": counties,
        "page": "profile",
    }
    # user is logged in & user is looking for his own profile #
    return render(request, "login/user_profile.html", context)


def user_privacy(request, username):
    try:
        userdata = UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "submit_change" in request.POST:

        privacy = Privacy.objects.get(username=username)
        circles = CircleUser.objects.filter(username=username)

        if ("vaccination_status_yes") in request.POST:
            privacy.show_vacination = True
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 1, True)

        if ("vaccination_status_no") in request.POST:
            privacy.show_vacination = False
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 1, False)

        if ("people_met_yes") in request.POST:
            privacy.show_people_met = True
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 2, True)

        if ("people_met_no") in request.POST:
            privacy.show_people_met = False
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 2, False)

        if ("locaiton_visited_yes") in request.POST:
            privacy.show_location_visited = True
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 3, True)

        if ("locaiton_visited_no") in request.POST:
            privacy.show_location_visited = False
            for circle in circles:
                update_compliance(username, circle.circle_id.circle_id, 3, False)

        privacy.save()

    privacy = Privacy.objects.get(username=username)

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    current_streak = get_current_streak(userdata.username)
    streak_yesterday = check_uploaded_yesterday(username)

    context = {
        "page_name": username,
        "username": current_username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        "current_streak": current_streak,
        "streak_yesterday": streak_yesterday,
        # other
        "session_valid": True,
        "privacy": privacy,
        "page": "privacy",
    }

    return render(request, "login/user_privacy.html", context)


def user_change_password(request, username):
    try:
        current_username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
        if current_username != username:
            raise Exception()
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "submit_change" in request.POST:
        hasher = PBKDF2WrappedSHA1PasswordHasher()
        userdata = UserData.objects.get(username=username)
        try:
            if userdata.password != hasher.encode(
                request.POST.get("old_password"), "test123"
            ) and userdata.password != request.POST.get("new_password"):
                raise Exception()
            try:
                if request.POST.get("new_password") != request.POST.get(
                    "confirm_password"
                ):
                    raise Exception()

                userdata.password = hasher.encode(
                    request.POST.get("confirm_password"), "test123"
                )
                userdata.save()
                messages.success(request, "Password Updated! ")

            except Exception:
                messages.error(request, "Password did not match!")
        except Exception:
            messages.error(request, "Invalid Old Password")

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    current_streak = get_current_streak(userdata.username)
    streak_yesterday = check_uploaded_yesterday(username)

    context = {
        "page_name": username,
        "username": current_username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        "current_streak": current_streak,
        "streak_yesterday": streak_yesterday,
        # other
        "session_valid": True,
        "page": "password",
    }

    return render(request, "login/user_password.html", context)


def settings(request, username, page):
    if "profile" in page:
        return user_profile(request, username)
    elif "privacy" in page:
        return user_privacy(request, username)
    elif "password" in page:
        return user_change_password(request, username)
    else:
        url = reverse("login:error")
        return HttpResponseRedirect(url)


def index(request):
    current_session_valid = False
    if "user_key" in request.session.keys():
        current_session_valid = True
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
    if current_session_valid:
        context = {
            "page_name": "CoviGuard",
            "css_name": "login",
            "session_valid": current_session_valid,
            "username": username,
            "userdata": userdata,
            "index": True,
        }
    else:
        context = {
            "page_name": "CoviGuard",
            "css_name": "login",
            "session_valid": current_session_valid,
            "index": True,
        }
    return render(request, "login/index.html", context)


def signin(request):

    if "user_key" in request.session.keys():
        url = reverse("login:index")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "sign-in" in request.POST:
        try:
            username = request.POST.get("username")
            hasher = PBKDF2WrappedSHA1PasswordHasher()
            password = hasher.encode(request.POST.get("password"), "test123")

            user = UserData.objects.get(username=username)
            if user.password == password:
                user_enc = signing.dumps(username)
                request.session["user_key"] = user_enc
                # url = reverse("circle:dashboard", kwargs={"username": username})
                url = reverse("login:index")
                return HttpResponseRedirect(url)
            else:
                raise Exception("Invalid Password")
        except Exception:
            messages.error(request, "Invalid Username or Password")

    context = {"page_name": "Sign in"}
    return render(request, "login/signin.html", context)


def signup(request):

    if "user_key" in request.session.keys():
        url = reverse("login:index")
        return HttpResponseRedirect(url)

    context = {"page_name": "SignUp"}

    # try:
    if request.method == "POST" and "signup-button" in request.POST:

        if request.POST.get("password") != request.POST.get("confirmpassword"):
            messages.error(request, "Password Do Not Match!!")
            return render(request, "login/signup.html", context)

        try:
            UserData.objects.get(username=request.POST.get("username"))
            messages.error(request, "Username Already Exist!!")
            return render(request, "login/signup.html", context)

        except Exception:
            userdata = UserData()
            userdata.firstname = request.POST.get("firstname")
            userdata.lastname = request.POST.get("lastname")
            userdata.username = request.POST.get("username")
            userdata.email = request.POST.get("email")
            hasher = PBKDF2WrappedSHA1PasswordHasher()
            userdata.password = hasher.encode(request.POST.get("password"), "test123")
            userdata.save()

            privacy = Privacy()
            privacy.username = UserData.objects.get(
                username=request.POST.get("username")
            )
            privacy.save()

            alert = Alert()
            alert.username = UserData.objects.get(username=request.POST.get("username"))
            alert.save()

            return HttpResponseRedirect(reverse("login:signin"))
    # except Exception:
    #     url = reverse("login:error")
    #     return HttpResponseRedirect(url)

    return render(request, "login/signup.html", context)


def logout(request):
    try:
        del request.session["user_key"]
    except Exception:
        return HttpResponseRedirect(reverse("login:index"))

    return HttpResponseRedirect(reverse("login:index"))


def error(request):
    return render(request, "login/error.html")
