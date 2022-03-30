from django.test import TestCase, Client
from django.urls import reverse
from login.models import UserData
import datetime


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()
        self.sigin_url = reverse(
            "login:signin",
        )
        self.sigup_url = reverse(
            "login:signup",
        )
        self.error_url = reverse(
            "login:error",
        )
        self.logout_url = reverse(
            "login:logout",
        )
        self.profile_url = reverse(
            "login:profile",
            args=["EashanKaushik"],
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

    def test_check_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")

    def test_signin(self):
        response = self.client.get(self.sigin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/signin.html")

    def test_signup(self):
        response = self.client.get(self.sigup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/signup.html")

    def test_errr(self):
        response = self.client.get(self.error_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/error.html")
