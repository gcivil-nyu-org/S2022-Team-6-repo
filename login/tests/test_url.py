from django.test import SimpleTestCase
from django.urls import reverse, resolve
from login.views import index, signin, error, signup, profile_view, logout


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("login:index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_signin_url_is_resolved(self):
        url = reverse("login:signin")
        print(resolve(url))
        self.assertEquals(resolve(url).func, signin)

    def test_signup_url_is_resolved(self):
        url = reverse("login:signup")
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)

    def test_logout_url_is_resolved(self):
        url = reverse("login:logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout)

    def test_profile_url_is_resolved(self):
        url = reverse("login:profile", args=["username"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile_view)

    def test_error_url_is_resolved(self):
        url = reverse("login:error")
        print(resolve(url))
        self.assertEquals(resolve(url).func, error)
