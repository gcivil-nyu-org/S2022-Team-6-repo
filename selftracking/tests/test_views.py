from django.test import TestCase, Client
from selftracking.models import SelfTrack
from django.urls import reverse
import datetime


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.SelfTrackData = SelfTrack.objects.create(
            date_uploaded=datetime.datetime.now(),
            username="person1",
            user_met="met1",
            location_visited="11225",
        )
        self.selftrack_url = reverse(
            "selftracking:selftrack",
            args=["cs55"],
        )

    def add_self_track(self):
        response = self.client.get(self.selftrack_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "selftracking/self_track.html")
