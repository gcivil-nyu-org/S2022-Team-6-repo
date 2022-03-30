from django.test import TestCase, Client
from django.urls import reverse
from login.models import UserData
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
            work_address="1122",
            home_adress="1122",
        )
        self.user_monitor_url = reverse("monitor:user_monitor")

    def test_user_monitor(self):
        response = self.client.get(self.user_monitor_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "monitor/index.html")
