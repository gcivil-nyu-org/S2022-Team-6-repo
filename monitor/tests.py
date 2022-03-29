# from django.test import TestCase

# Create your tests here.
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import base


class TestUrls(SimpleTestCase):
    def test_base_url_is_resolved(self):
        url = reverse("monitor:user_monitor")
        print(resolve(url))
        self.assertEquals(resolve(url).func, base)
