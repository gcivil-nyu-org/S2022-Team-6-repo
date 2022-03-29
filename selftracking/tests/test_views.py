from django.test import TestCase, Client
from selftracking.models import SelfTrack
from django.urls import reverse
from login.models import UserData
import datetime


class TestViews(TestCase):
    def setUp(self):
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

    def test_add_self_track(self):
        response = self.client.get(self.selftrack_url)
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")
