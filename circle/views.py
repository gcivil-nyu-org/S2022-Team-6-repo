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
                # print(circleone.circle_id)

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
        # Other
        "circle_user_data": circle_user_data,
        "recent_circles": recent_circles,
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

    if request.method == "POST" and "remove_user" in request.POST:
        remove_user(username, request.POST.get("remove_user"), circle_id)

    circle_data = CircleUser.objects.get(circle_id=circle_id, username=username)

    add_recent_circle(circle_data)  # TODO: Recent Circle
    circle_user_data = CircleUser.objects.filter(circle_id=circle_id)
    circle_policy = CirclePolicy.objects.filter(circle_id=circle_id)

    circle_compliance = get_circle_compliance(circle_id=circle_id)

    policies = []
    for policy in circle_policy:
        policies.append(policy.policy_id)

    request_user_data, requests = get_notifications(username=username)
    three_non_compliance, non_compliance = get_all_non_compliance(username, True)

    total_notify = requests + non_compliance

    if circle_data.is_admin:
        circle_request = get_circle_requests(circle_id)
    else:
        circle_request = None

    streak_today = check_upload_today(username)

    context = {
        "page_name": circle_data.circle_id.circle_name,
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        # Other
        "circle_user_data": circle_user_data,
        "circle_data": circle_data,
        "circle_request": circle_request,
        "is_admin": circle_data.is_admin,
        "policies": policies,
        "circle_compliance": circle_compliance,
        # "group_image": group_image,
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

    context = {
        "page_name": "Add Circle",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
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

    context = {
        "page_name": "Notifications",
        "username": username,
        "userdata": userdata,
        "request_user_data": request_user_data,
        "total_notify": total_notify,
        "three_non_compliance": three_non_compliance,
        "streak_today": streak_today,
        # Other
        "all_requests": all_requests,
        "all_non_compliance": all_non_compliance,
    }

    return render(request, "circle/notifications.html", context)

def search_circles(request):
    if request.method == "POST":
        searched = request.POST['searched']
        Searched_circle = Circle.objects.filter(circle_name__contains=searched)
        return render(request, 'circle/search_circles.html', {'searched':searched,'Searched_circle':Searched_circle})

def exit_circle(request, username, circle_id):
    admin_user = CircleUser.objects.filter(circle_id=circle_id, is_admin=True)
    remove_user(admin_user[0].username.username, username, circle_id)

    url = reverse("circle:dashboard", kwargs={"username": username})
    return HttpResponseRedirect(url)


def delete_circle(request, username, circle_id):
    remove_circle(circle_id)

    url = reverse("circle:dashboard", kwargs={"username": username})
    return HttpResponseRedirect(url)
