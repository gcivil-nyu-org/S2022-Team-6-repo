from django.test import TestCase, Client
from django.urls import reverse
from login.models import UserData
from alert.models import Alert
import datetime


class TestViews(TestCase):
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
        )

        self.alert = Alert.objects.create(
            username=self.userdata,
        )

        self.user_monitor_url = reverse("monitor:user_monitor")
        self.client2 = Client()
        self.session2 = self.client2.session
        self.session2["user_key"] = None
        self.session2.save()

    def test_user_monitor(self):
        response = self.client.get(self.user_monitor_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_user_monitor_url(self):
        response = self.client.get(self.user_monitor_url)
        print(response)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "monitor/index.html")

    def test_user2_monitor(self):
        response = self.client2.get(self.user_monitor_url)
        self.assertEqual(response.status_code, 302)
        url = reverse("login:error")
        # print(response.url)
        # print(url)
        self.assertEqual(url, response.url)
