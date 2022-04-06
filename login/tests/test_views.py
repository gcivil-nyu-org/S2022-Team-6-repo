from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from login.models import UserData
import datetime


class TestViews(TestCase, TransactionTestCase):
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
        self.profile_url_error = reverse(
            "login:profile",
            args=["WrongUser"],
        )
        self.profile_url_error_1 = reverse(
            "login:profile",
            args=["ChinmayKulkarni"],
        )
        self.index_url = reverse("login:index")

        self.user_profile_url = reverse("login:user_profile", args=["EashanKaushik"])

        self.user_profile_url_error = reverse("login:user_profile", args=[1])

        self.user_profile_url_error_2 = reverse(
            "login:user_profile", args=["ChinmayKulkarni"]
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
        self.userdata2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.profile_url_fake = reverse(
            "login:profile",
            args=[None],
        )

    def test_check_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/profile.html")

    def test_signin(self):
        response = self.client.post(
            self.sigin_url,
            data={"sign-in": "", "username": "EashanKaushik", "password": "coviguard"},
        )
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.get(self.sigup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/signup.html")

    def test_errr(self):
        response = self.client.get(self.error_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/error.html")

    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "login/error.html")

    def test_index_url(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/index.html")

    def test_check_profile_fake(self):
        response = self.client.get(self.profile_url_fake)
        # print(response.status_code)
        # print(response)
        self.assertEqual(response.status_code, 302)
        url = reverse("login:error")
        self.assertEqual(url, response.url)

    def test_index_url_false(self):
        response = self.client.get(self.index_url)
        self.current_session_valid = False
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/index.html")

    def test_check_profile_error(self):
        response = self.client.get(self.profile_url_error)
        self.assertEqual(response.status_code, 302)

    def test_user_not_logged_in(self):
        self.session.pop("user_key")
        self.session.save()
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/index.html")

    def test_signin_withWorngPassword(self):
        response = self.client.post(
            self.sigin_url,
            data={
                "sign-in": "",
                "username": "EashanKaushik",
                "password": "wrongPassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/signin.html")

    def test_profileView_WithDifferentUser(self):
        response = self.client.get(self.profile_url_error_1)
        self.assertEqual(response.status_code, 200)

    def test_user_profile(self):
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")

    def test_user_profile_error(self):
        response = self.client.get(self.user_profile_url_error)
        self.assertEqual(response.status_code, 302)

    def test_user_profile_error_2(self):
        response = self.client.get(self.user_profile_url_error_2)
        self.assertEqual(response.status_code, 302)


class AtomicTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.user_profile_url = reverse("login:user_profile", args=["EashanKaushik"])

        self.user_profile_url_error = reverse("login:user_profile", args=[1])

        self.user_profile_url_error_2 = reverse(
            "login:user_profile", args=["ChinmayKulkarni"]
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
        self.userdata2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

    def test_user_profile_post(self):
        response = self.client.post(
            self.user_profile_url,
            data={
                "submit_change": "",
                "first_name": "Eashan",
                "last_name": "Kaushik",
                "dob": datetime.datetime.now(),
                "phone": "1234567890",
                "home": "1122",
                "work": "1122",
                "vaccination_status_yes": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")

    def test_user_profile_post_error_field(self):
        response = self.client.post(
            self.user_profile_url,
            data={
                "submit_change": "",
                "first_name": "",
                "last_name": "Kaushik",
                "dob": [1],
                "phone": "12345",
                "home": "1122",
                "work": "1122",
                "vaccination_status_yes": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")
