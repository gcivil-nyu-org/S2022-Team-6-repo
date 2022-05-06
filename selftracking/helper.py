from .models import SelfTrack
import datetime
from circle.models import CircleUser


def check_date_uplaoded(username, default=True):
    #     return (
    #         SelfTrack.objects.filter(username=username)
    #         .latest("date_uploaded")
    #         .date_uploaded.date()
    #         == datetime.datetime.now().date()
    #         and SelfTrack.objects.filter(username=username)
    #         .latest("date_uploaded")
    #         .user_met
    #         != "42a7b2626eae970122e01f65af2f5092"
    #     )
    # else:
    return (
        SelfTrack.objects.filter(username=username)
        .latest("date_uploaded")
        .date_uploaded.date()
        == datetime.datetime.now().date()
    )


def check_upload_today(username):
    try:
        if len(SelfTrack.objects.filter(username=username)) == 0:
            raise Exception()
    except Exception:
        return False

    latest = SelfTrack.objects.filter(username=username).latest("date_uploaded")
    return latest.date_uploaded.date() == datetime.datetime.now().date()


def check_uploaded_yesterday(username):

    yesterday_date = datetime.date.today() + datetime.timedelta(days=-1)

    if len(SelfTrack.objects.filter(username=username)) > 0:

        return (
            SelfTrack.objects.filter(username=username)
            .latest("date_uploaded")
            .date_uploaded.date()
            == yesterday_date
            and SelfTrack.objects.filter(username=username)
            .latest("date_uploaded")
            .user_met
            != "42a7b2626eae970122e01f65af2f5092"
        )
    else:
        return False


def get_current_streak(username):
    selftrack = SelfTrack.objects.filter(username=username)
    if len(selftrack) > 0:
        return selftrack.latest("date_uploaded").streak
    else:
        return 0


def get_longest_streak(username):
    return (
        SelfTrack.objects.filter(username=username)
        .latest("date_uploaded")
        .largest_streak
    )


def get_all_connections(username):
    connections = set()

    for circle in CircleUser.objects.filter(username=username):

        current_circle_id = circle.circle_id.circle_id

        for user in CircleUser.objects.filter(circle_id=current_circle_id):
            if user.username.username != username:
                connections.add(user.username.username)

    if len(connections) == 0:
        return None

    return connections
