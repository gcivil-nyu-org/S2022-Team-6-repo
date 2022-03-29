from django.test import TestCase, Client
from django.urls import reverse
from circle.models import Circle, CircleUser, RecentCircle
from login.models import UserData
import datetime


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.dashboard_url = reverse(
            "circle:dashboard",
            args=["EashanKaushik"],
        )

        self.user_circle_url = reverse(
            "circle:user_circle",
            args=["EashanKaushik", "1"],
        )

        self.create_url = reverse(
            "circle:create",
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

        self.recentcircle = RecentCircle.objects.create(
            username=self.userdata, recent_circle="[1]"
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
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/circle.html")

        response = self.client.get(self.user_circle_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/current-circle.html")

        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/add.html")
