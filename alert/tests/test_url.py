from django.test import SimpleTestCase
from django.urls import reverse, resolve
from alert.views import alert_user
from circle.views import (
    circle,
    current_circle,
    create,
    notify,
    exit_circle,
    delete_circle,
)


class TestUrls(SimpleTestCase):
    def test_dashboard_url(self):
        url = reverse("circle:dashboard", args=["username"])
        self.assertEquals(resolve(url).func, circle)
