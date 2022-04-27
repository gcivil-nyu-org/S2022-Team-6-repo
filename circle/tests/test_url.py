from django.test import SimpleTestCase
from django.urls import reverse, resolve
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
        url = reverse("circle:dashboard", args=["username", "query"])
        self.assertEquals(resolve(url).func, circle)

    def test_user_circle_url(self):
        url = reverse("circle:user_circle", args=["username", "circleid"])
        self.assertEquals(resolve(url).func, current_circle)

    def test_create_circle_url(self):
        url = reverse("circle:create")
        self.assertEquals(resolve(url).func, create)

    def test_notify_url(self):
        url = reverse("circle:notify", args=["username"])
        self.assertEquals(resolve(url).func, notify)

    def test_exit_circle_url(self):
        url = reverse("circle:exitcircle", args=["username", "circleid"])
        self.assertEquals(resolve(url).func, exit_circle)

    def test_delete_circle_url(self):
        url = reverse("circle:deletecircle", args=["username", "circleid"])
        self.assertEquals(resolve(url).func, delete_circle)
