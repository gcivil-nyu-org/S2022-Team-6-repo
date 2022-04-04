import datetime


def convert_datetime(current_date):
    current_date = (datetime.datetime.strptime(current_date, "%Y-%m-%d")).date()

    return current_date.strftime("%b %d")
