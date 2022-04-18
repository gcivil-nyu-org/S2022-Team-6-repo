from django.test import TestCase, Client
from selftracking.models import SelfTrack
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
            work_address="1122",
            home_adress="1122",
        )

        self.alert = Alert.objects.create(
            username=self.userdata,
        )

        self.selftrack_data = SelfTrack.objects.create(
            date_uploaded=datetime.datetime.now(),
            username=self.userdata,
            user_met="met1",
            location_visited="11225",
            streak=9,
            largest_streak=10,
        )
        self.SelfTrackData = SelfTrack.objects.create(
            date_uploaded=datetime.datetime.now(),
            username=self.userdata,
            user_met="met1",
            location_visited="11225",
        )
        self.selftrack_url = reverse(
            "selftracking:selftrack",
            args=["cs55"],
        )

        self.selftrack_url_real = reverse(
            "selftracking:selftrack",
            args=["EashanKaushik"],
        )
        self.client2 = Client()
        self.session2 = self.client2.session
        self.session2["user_key"] = None
        self.session2.save()
        self.selftrack_url_real2 = reverse(
            "selftracking:selftrack",
            args=[None],
        )

    def test_add_self_track(self):
        response = self.client.get(self.selftrack_url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_add_self_track_real(self):
        response = self.client.get(self.selftrack_url_real)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_getself_track(self):
        # Issue a GET request.
        response = self.client.get("selftracking/self_track.html")
        # print(response)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")
        self.assertEqual(response.status_code, 404)

    def test_add_selftrack(self):

        response = self.client.post(
            {"username": "name", "user_met": "pass", "location_visited": "1225"}
        )

        self.assertNotEqual(response.status_code, 302)

    def test_selftrack_data(self):
        response = self.client.get(self.selftrack_url_real)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_user2_monitor(self):
        response = self.client2.get(self.selftrack_url_real2)
        self.assertEqual(response.status_code, 302)
        url = reverse("login:error")
        # print(response.url)
        # print(url)
        self.assertEqual(url, response.url)
