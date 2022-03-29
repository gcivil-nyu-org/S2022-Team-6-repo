from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from selftracking.views import selftrack
from selftracking.models import SelfTrack


class TestUrls(SimpleTestCase):
    def test_selftrack_url(self):
        url = reverse("selftracking:selftrack", args=["username"])
        self.assertEquals(resolve(url).func, selftrack)
