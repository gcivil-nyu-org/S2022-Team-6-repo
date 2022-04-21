from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse
from django.template.loader import render_to_string

from .models import Circle, CirclePolicy, CircleUser, RequestCircle
from login.models import UserData

from .helper import (
    get_notifications,
    get_circle_requests,
    get_all_non_compliance,
    get_circle_compliance,
    get_recent_circles,
    check_recent_circle,
    get_user_alert,
    check_vacination_policy,
    streak_uploaded,
)
from .driver import (
    create_request,
    create_circle,
    accept_request,
    reject_request,
    remove_user,
    remove_circle,
    recent_circle,
    add_recent_circle,
)

from selftracking.helper import check_upload_today

from alert.helper import get_alert


from django.core import signing


def circle(request, username):
    try:
        userdata = UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    check_recent_circle(recent_circle(username), username)
    recent_circle_list = recent_circle(username)
    recent_circles = get_recent_circles(recent_circle_list, username)

    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)

    # AJAX
    search = request.GET.get("q")

    circles = list()
    if search:
        for circle_user in circle_user_data:

            circleone = Circle.objects.filter(
                circle_id=circle_user.circle_id.circle_id, circle_name__icontains=search
            )
            if circleone:
                circles.append(circle_user)

    ctx = {}
    ctx["circles"] = circles

    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and does_req_accept_json
    )

    if is_ajax_request:
        if len(circles) != 0:
            html = render_to_string(
                template_name="circle-search.html",
                context={
                    "page_name": "Circle",
                    "username": username,
                    "userdata": userdata,
                    "request_user_data": request_user_data,
                    "total_notify": total_notify,
                    "three_non_compliance": three_non_compliance,
                    "streak_today": streak_today,
                    "alert": alert,
                    # other
                    "circles": circles,
                    "recent_circles": recent_circles,
                },
            )
        else:
            html = render_to_string(
                template_name="circle-search.html",
                context={
                    "page_name": "Circle",
                    "username": username,
                    "userdata": userdata,
                    "request_user_data": request_user_data,
                    "total_notify": total_notify,
                    "three_non_compliance": three_non_compliance,
                    "streak_today": streak_today,
                    "alert": alert,
                    # other
                    "circle_user_data": circle_user_data,
                    "recent_circles": recent_circles,
                },
            )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    context = {
        "page_name": "Circle",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # Other
        "circle_user_data": circle_user_data,
        "recent_circles": recent_circles,
        "circle": True,
        # "qs_json": json.dumps(list(circle_user_data.values())),
    }

    return render(request, "circle/circle.html", context)


def current_circle(request, username, circle_id):
    try:
        userdata = UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
        CircleUser.objects.get(circle_id=circle_id, username=current_username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    search = False
    searched_user = list()
    search_user_found = False

    # Delete Request for user
    if request.method == "POST" and "remove_user" in request.POST:
        remove_user(username, request.POST.get("remove_user"), circle_id)

    # Search user
    if request.method == "POST" and "search-users-submit" in request.POST:
        search = True
        search_query = request.POST.get("search-users")
        users_found = UserData.objects.filter(username__icontains=search_query)

        searched_user = list()
        search_user_found = False

        for user_found in users_found.iterator():

            try:
                search_user = CircleUser.objects.get(
                    circle_id=circle_id, username=user_found
                )
                search_user_found = True
                searched_user.append(search_user)
            except Exception:
                pass

        if not search_user_found > 0:
            messages.error(request, f"No Username {search_query}!")

    # Get CircleUser object for username
    circle_data = CircleUser.objects.get(circle_id=circle_id, username=username)

    # add to recent circle, get circle user data
    add_recent_circle(circle_data)
    circle_user_data = CircleUser.objects.filter(circle_id=circle_id)

    # check last streak uploaded
    streak_last_updated, stread_date_updated = streak_uploaded(circle_id=circle_id)

    # circle policies for header
    policies = []
    for policy in CirclePolicy.objects.filter(circle_id=circle_id):
        policies.append(policy.policy_id)

    # check user alerts
    user_alert, user_alert_data = get_user_alert(circle_id=circle_id)

    # circle compliance status
    circle_compliance, is_compliant = get_circle_compliance(circle_id=circle_id)
    # {
    #     username: 'Compliant'/ 'Non Compliant',
    # ...
    # }

    # check if vaccination policy needs to be uploaded
    check_vacinated_policy = check_vacination_policy(circle_id=circle_id)
    # if circle admin show number of pending request
    if circle_data.is_admin:
        circle_request = get_circle_requests(circle_id)
    else:
        circle_request = None

    # Navbar Data
    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)
    total_notify = requests + non_compliance
    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    context = {
        "page_name": circle_data.circle_id.circle_name,
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # Other
        "search_user_found": search_user_found,
        "searched_user": searched_user,
        "search": search,
        "circle_user_data": circle_user_data,
        "circle_data": circle_data,
        "circle_request": circle_request,
        "is_admin": circle_data.is_admin,
        "policies": policies,
        "circle_compliance": circle_compliance,
        "is_compliant": is_compliant,
        "user_alert": user_alert,
        "user_alert_data": user_alert_data,
        "check_vacinated_policy": check_vacinated_policy,
        "stread_date_updated": stread_date_updated,
        "streak_last_updated": streak_last_updated,
    }

    return render(request, "circle/current-circle.html", context)


def create(request):

    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "request_circle" in request.POST:
        circle_id = request.POST.get("circle_id")
        try:
            Circle.objects.get(circle_id=circle_id)
            try:
                RequestCircle.objects.get(circle_id=circle_id, username=username)
                messages.error(request, "Request Pending!")
            except Exception:
                try:
                    CircleUser.objects.get(username=username, circle_id=circle_id)
                    messages.error(request, "Already a Member!")
                except Exception:
                    create_request(username, circle_id)
                    messages.success(request, "Request sent to Circle Admin")
        except Exception:
            messages.error(request, "Circle ID does not exist!")

    if request.method == "POST" and "create_circle" in request.POST:

        circle_name = request.POST.get("circle_name")
        try:
            create_circle(
                username,
                circle_name,
                request.POST.getlist("policy_id"),
                request.FILES["circle_image"],
            )
        except Exception:
            create_circle(
                username, circle_name, request.POST.getlist("policy_id"), None
            )

    circle_user_data = CircleUser.objects.filter(username=username)

    request_user_data, requests = get_notifications(username=username)

    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    streak_today = check_upload_today(username)
    alert = get_alert(username=username)
    context = {
        "page_name": "Add Circle",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # Other
        "circle_user_data": circle_user_data,
    }

    return render(request, "circle/add.html", context)


def notify(request):

    try:
        username = signing.loads(request.session["user_key"])
        userdata = UserData.objects.get(username=username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "accept_circle" in request.POST:
        accept_request(request.POST.get("accept_circle"))

    if request.method == "POST" and "reject_circle" in request.POST:
        reject_request(request.POST.get("reject_circle"))

    request_user_data, requests = get_notifications(username=username, get_three=True)
    all_requests, _ = get_notifications(username=username, get_three=False)

    three_non_compliance, non_compliance = get_all_non_compliance(username, True)
    all_non_compliance, _ = get_all_non_compliance(username, False)

    total_notify = requests + non_compliance

    streak_today = check_upload_today(username)
    alert = get_alert(username=username)

    context = {
        "page_name": "Notifications",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # Other
        "all_requests": all_requests,
        "all_non_compliance": all_non_compliance,
    }

    return render(request, "circle/notifications.html", context)


def exit_circle(request, username, circle_id):

    try:
        UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
        CircleUser.objects.get(circle_id=circle_id, username=current_username)
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    admin_user = CircleUser.objects.filter(circle_id=circle_id, is_admin=True)
    remove_user(admin_user[0].username.username, username, circle_id)

    url = reverse("circle:dashboard", kwargs={"username": username})
    return HttpResponseRedirect(url)


def delete_circle(request, username, circle_id):

    try:
        UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
        CircleUser.objects.get(
            circle_id=circle_id, is_admin=True, username=current_username
        )
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    remove_circle(circle_id)

    url = reverse("circle:dashboard", kwargs={"username": username})
    return HttpResponseRedirect(url)


def edit_permission(request, username, circle_id):

    try:
        userdata = UserData.objects.get(username=username)
        current_username = signing.loads(request.session["user_key"])
        if current_username != username:
            raise Exception()
        CircleUser.objects.get(
            circle_id=circle_id, is_admin=True, username=current_username
        )
    except Exception:
        url = reverse("login:error")
        return HttpResponseRedirect(url)

    if request.method == "POST" and "circle_update" in request.POST:

        circle_data = Circle.objects.get(circle_id=circle_id)

        circle_data.circle_name = request.POST.get("circle_name")

        print(request.FILES)

        if request.FILES:
            print("hello")
            circle_image = request.FILES["circle_image"]
            print(type(circle_image))
            circle_image.name = (
                str(circle_data.circle_id) + "." + circle_image.name.split(".")[-1]
            )
            print(circle_image.name)
            circle_data.group_image = circle_image

        circle_data.save()

    circle_data = Circle.objects.get(circle_id=circle_id)

    request_user_data, requests = get_notifications(username=username)

    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    streak_today = check_upload_today(username)
    alert = get_alert(username=username)

    context = {
        "page_name": "Edit Permission",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        "alert": alert,
        # other
        "circle_data": circle_data,
    }

    return render(request, "circle/edit_permission.html", context)
