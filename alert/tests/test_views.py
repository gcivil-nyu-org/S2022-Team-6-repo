from django.test import TestCase, Client
from django.urls import reverse
from login.models import UserData
from alert.models import Alert
from alert.driver import (
    home_alert,
    work_alert,
    people_met_alert,
    location_visited_alert,
)
from monitor.driver import get_s3_client, get_data
from selftracking.models import SelfTrack
import datetime


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.userdata = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.userdata_2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.alert = Alert.objects.create(
            username=self.userdata,
        )
        self.alert_2 = Alert.objects.create(
            username=self.userdata_2,
        )

        self.selftrack = SelfTrack.objects.create(
            date_uploaded=(
                datetime.date.today() + datetime.timedelta(days=-1)
            ).strftime("%Y-%m-%d"),
            username=self.userdata,
            user_met="ChinmayKulkarni",
            location_visited="New York City",
        )

        # self.client2 = Client()
        # self.session2 = self.client2.session
        # self.session2["user_key"] = None
        # self.session2.save()

        self.alert_url = reverse(
            "alert:alert_user",
            args=["EashanKaushik"],
        )

        self.markAllAsRead_url = reverse(
            "alert:markAllRead",
            args=["EashanKaushik"],
        )

    def test_user2_circle(self):
        response = self.client.get(self.alert_url)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        # url = reverse("login:error")
        # self.assertEqual(url, response.url)

    def test_alerts(self):
        response = self.client.get(self.alert)
        self.assertEqual(response.status_code, 404)

    def test_alert_user(self):
        response = self.client.get(self.alert_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "alert/alert.html")

    def test_alert_user_error(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.get(self.alert_url)
        self.assertEqual(response.status_code, 302)

    def test_markAllRead(self):
        response = self.client.get(self.markAllAsRead_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "alert/alert.html")

    def test_markAllRead_error(self):
        self.session["user_key"] = ""
        self.session.save()
        response = self.client.get(self.markAllAsRead_url)
        self.assertEqual(response.status_code, 302)

    def test_driver_homelocation(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        home_alert("New York City", historical, yesterday)

    def test_driver_worklocation(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        work_alert("New York City", historical, yesterday)

    def test_driver_peoplemet(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        people_met_alert('["ChinmayKulkarni"]', historical, yesterday)

    def test_driver_nopeoplemet(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        people_met_alert("[]", historical, yesterday)

    def test_driver_location(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        location_visited_alert('["New York City"]', historical, yesterday)

    def test_driver_nolocation(self):
        try:
            _, client_object = get_s3_client()
            historical, _, _ = get_data(client_object)
        except Exception:  # pragma: no cover
            self.assertEqual("True", "Flase")  # pragma: no cover
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        location_visited_alert("[]", historical, yesterday)
