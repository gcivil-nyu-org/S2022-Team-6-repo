from django.test import SimpleTestCase
from django.urls import reverse, resolve
from selftracking.views import selftrack


class TestUrls(SimpleTestCase):
    def test_selftrack_url(self):
        url = reverse("selftracking:selftrack", args=["username"])
        self.assertEquals(resolve(url).func, selftrack)
