from django.test import SimpleTestCase
from django.urls import reverse, resolve
from alert.views import alert_user


class TestUrls(SimpleTestCase):
    def test_dashboard_url(self):
        url = reverse("alert:alert_user", args=["username"])
        self.assertEquals(resolve(url).func, alert_user)
