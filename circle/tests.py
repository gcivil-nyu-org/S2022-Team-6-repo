from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import circle, current_circle, create

class TestUrls(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        url = reverse("circle:dashboard",args=['sv5'])
        print(resolve(url))
        self.assertEquals(resolve(url).func,circle)

    def test_current_circle_url_is_resolved(self):
        url = reverse("circle:user_circle",args=['asd873g','sv5',7])
        print(resolve(url))
        self.assertEquals(resolve(url).func,current_circle)

    def test_current_createcircle_url_is_resolved(self):
        url = reverse("circle:create",args=['asd873g'])
        print(resolve(url))
        self.assertEquals(resolve(url).func,create)
