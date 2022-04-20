from django.test import TestCase, Client
from django.urls import reverse
from login.models import UserData
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

        self.client2 = Client()
        self.session2 = self.client2.session
        self.session2["user_key"] = None
        self.session2.save()

        self.alert_url = reverse(
            "alert:alert_user",
            args=["EashanKaushik"],
        )

    def test_user2_circle(self):
        response = self.client2.get(self.alert_url)
        # print(response.status_code)
        self.assertEqual(response.status_code, 302)
        url = reverse("login:error")
        self.assertEqual(url, response.url)