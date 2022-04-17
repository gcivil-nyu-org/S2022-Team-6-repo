from django.core.management.base import BaseCommand

from alert.models import Alert
from selftracking.models import SelfTrack
from login.models import UserData

from alert.driver import (
    home_alert,
    work_alert,
    people_met_alert,
    location_visited_alert,
    get_model_data,
)
from monitor.driver import get_s3_client, get_data


import datetime


class Command(BaseCommand):
    help = "Update the Alert for all users"

    def handle(self, *args, **options):
        # TODO: Try Catch block
        # try:
        _, client_object = get_s3_client()
        historical, _, _ = get_data(client_object)

        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        ten_days_from_today = (
            datetime.date.today() + datetime.timedelta(days=-11)
        ).strftime("%Y-%m-%d")

        historical = historical[historical.state == "New York"]
        historical = historical[
            (historical.date <= yesterday) & (historical.date >= ten_days_from_today)
        ]

        alerts = Alert.objects.all()

        data_alert_case = list()
        data_alert_death = list()
        location_alert_case = False
        location_alert_death = False
        home_address_case = False
        home_address_death = False
        work_address_case = False
        work_address_death = False
        people_data = list()
        people_alert = False

        for alert in alerts:

            username = alert.username.username

            self.stdout.write(self.style.SUCCESS(f"Initial Alert: {username}"))

            # Location visited
            location_visited = SelfTrack.objects.filter(
                username=username,
                date_uploaded__date=datetime.datetime.now().date()
                + datetime.timedelta(days=-1),
            )

            try:
                if (
                    location_visited[0].location_visited
                    != "42a7b2626eae970122e01f65af2f5092"
                ):
                    (
                        data_alert_case,
                        data_alert_death,
                        location_alert_case,
                        location_alert_death,
                    ) = location_visited_alert(
                        location_visited[0].location_visited, historical, yesterday
                    )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        f"Location visited for {username} does not exist for {yesterday}."
                    )
                )

            # Home Address
            try:
                if UserData.objects.get(username=username).home_adress:
                    home_address_case, home_address_death = home_alert(
                        UserData.objects.get(username=username).home_adress,
                        historical,
                        yesterday,
                    )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(f"Home Address for {username} does not exist.")
                )
            # Work Address
            try:
                if UserData.objects.get(username=username).work_address:
                    work_address_case, work_address_death = work_alert(
                        UserData.objects.get(username=username).work_address,
                        historical,
                        yesterday,
                    )
            except Exception:
                self.stdout.write(
                    self.style.ERROR(f"Work Address for {username} does not exist.")
                )

            # Alert New Model - Save
            user_alert = Alert.objects.get(username=username)

            user_alert.location_alert_case = (
                user_alert.location_alert_case or location_alert_case
            )
            user_alert.location_alert_death = (
                user_alert.location_alert_death or location_alert_death
            )
            user_alert.home_alert_case = user_alert.home_alert_case or home_address_case
            user_alert.home_alert_death = (
                user_alert.home_alert_death or home_address_death
            )
            user_alert.work_alert_case = user_alert.work_alert_case or work_address_case
            user_alert.work_alert_death = (
                user_alert.work_alert_death or work_address_death
            )

            user_alert.location_data_case = get_model_data(data_alert_case)
            user_alert.location_data_death = get_model_data(data_alert_death)

            user_alert.alert = (
                user_alert.alert
                or location_alert_case
                or location_alert_death
                or home_address_case
                or home_address_death
                or work_address_case
                or work_address_death
            )

            user_alert.save()

        for alert in alerts:
            # People Met
            username = alert.username.username

            self.stdout.write(self.style.SUCCESS(f"People met Alert: {username}"))

            people_met = SelfTrack.objects.filter(
                username=username,
                date_uploaded__date=datetime.datetime.now().date()
                + datetime.timedelta(days=-1),
            )
            try:
                if people_met[0].people_met != "42a7b2626eae970122e01f65af2f5092":

                    people_data, people_alert = people_met_alert(
                        people_met[0].people_met, historical, yesterday
                    )

            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        f"People visited for {username} does not exist for {yesterday}."
                    )
                )

            # Alert Model - Save
            user_alert = Alert.objects.get(username=username)

            user_alert.people_data = get_model_data(people_data)
            user_alert.people_alert = user_alert.people_alert or people_alert

            user_alert.alert = user_alert.alert or people_alert

            user_alert.save()

        # except Exception:
        #     self.stdout.write(self.style.ERROR('Internal Error - EK'))
        #     return

        self.stdout.write(self.style.SUCCESS("Successfully printed all Book titles"))
        return
