from .models import SelfTrack
import datetime


def check_date_uplaoded(username):
    return (
        SelfTrack.objects.filter(username=username)
        .latest("date_uploaded")
        .date_uploaded.date()
        == datetime.datetime.now().date()
    )


def check_uploaded_yesterday(username):

    yesterday_date = datetime.date.today() + datetime.timedelta(days=-1)

    return (
        SelfTrack.objects.filter(username=username)
        .latest("date_uploaded")
        .date_uploaded.date()
        == yesterday_date
    )


def get_current_streak(username):

    return SelfTrack.objects.filter(username=username).latest("date_uploaded").streak
