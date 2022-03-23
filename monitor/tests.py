# from django.test import TestCase

# Create your tests here.
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from .views import base


class TestUrls(SimpleTestCase):
    def test_base_url_is_resolved(self):
        url = reverse("monitor:user_monitor", args=["asda723h"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, base)


class TestViews(TestCase):
    def test_get_data(self):
        client = Client()
        response = client.get(reverse("monitor:user_monitor"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "monitor/index.html")
