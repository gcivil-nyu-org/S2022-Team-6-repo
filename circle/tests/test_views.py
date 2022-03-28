from django.test import TestCase, Client
from django.urls import reverse
from circle.models import Circle, CircleUser
from login.models import UserData
import datetime


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse(
            "circle:dashboard",
            args=[
                "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
            ],
        )
        self.userdata = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.circle = Circle.objects.create(
            circle_id=1,
            circle_name="TestCircle",
            admin_username=self.userdata,
            no_of_users=1,
        )
        self.circle_user_data = CircleUser.objects.create(
            circle_id=self.circle, username=self.userdata, is_admin=True, is_member=True
        )

    def test_circle(self):
        response = self.client.get(self.dashboard_url)
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/circle.html")
