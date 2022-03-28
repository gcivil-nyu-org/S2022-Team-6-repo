from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import index, signin, error


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("login:index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_signin_url_is_resolved(self):
        url = reverse("login:signin")
        print(resolve(url))
        self.assertEquals(resolve(url).func, signin)

    def test_error_url_is_resolved(self):
        url = reverse("login:error")
        print(resolve(url))
        self.assertEquals(resolve(url).func, error)
