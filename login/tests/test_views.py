from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from login.models import UserData, Privacy
from circle.models import Circle, CircleUser, Policy, CirclePolicyCompliance
import datetime
from login.hashes import PBKDF2WrappedSHA1PasswordHasher
import os
from pathlib import Path


class TestViews(TestCase, TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.hasher = PBKDF2WrappedSHA1PasswordHasher()

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

        self.privacy_url = reverse("login:privacy", args=["EashanKaushik"])

        self.privacy_url_error = reverse("login:privacy", args=["ChinmayKulkarni"])

        self.change_password_url = reverse(
            "login:change_password", args=["EashanKaushik"]
        )

        self.change_password_url_error = reverse(
            "login:change_password", args=["ChinmayKulkarni"]
        )

        self.settings_profile_url = reverse(
            "login:settings", args=["EashanKaushik", "profile"]
        )

        self.settings_privacy_url = reverse(
            "login:settings", args=["EashanKaushik", "privacy"]
        )

        self.settings_password_url = reverse(
            "login:settings", args=["EashanKaushik", "password"]
        )

        self.settings_error_url = reverse(
            "login:settings", args=["EashanKaushik", "Error"]
        )

        self.userdata = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password=self.hasher.encode("coviguard", "test123"),
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.userdata2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password=self.hasher.encode("coviguard", "test123"),
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.privacy = Privacy.objects.create(
            username=self.userdata,
            show_vacination=True,
            show_people_met=True,
            show_location_visited=False,
        )

        self.profile_url_fake = reverse(
            "login:profile",
            args=[None],
        )

    def test_check_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")

    def test_check_profile_2(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/profile-general.html")

    def test_signin(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.post(
            self.sigin_url,
            data={"sign-in": "", "username": "EashanKaushik", "password": "coviguard"},
        )
        self.assertEqual(response.status_code, 302)

    def test_signup(self):
        del self.session["user_key"]
        self.session.save()
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

    def test_logout_2(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

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
        del self.session["user_key"]
        self.session.save()
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

    def test_user_privacy(self):
        response = self.client.get(self.privacy_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_privacy.html")

    def test_user_privacy_error(self):
        response = self.client.get(self.privacy_url_error)
        self.assertEqual(response.status_code, 302)

    def test_user_change_password(self):
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_password.html")

    def test_user_change_password_error(self):
        response = self.client.get(self.change_password_url_error)
        self.assertEqual(response.status_code, 302)

    def test_user_change_password_post_error1(self):
        response = self.client.post(
            self.change_password_url,
            data={
                "submit_change": "",
                "old_password": "covi",
                "new_password": "coviguard",
                "confirm_password": "coviguard",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_user_change_password_post_error2(self):
        response = self.client.post(
            self.change_password_url,
            data={
                "submit_change": "",
                "old_password": "coviguard",
                "new_password": "coviguard",
                "confirm_password": "covi",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_user_settings_profile(self):
        response = self.client.get(self.settings_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_profile.html")

    def test_user_settings_privacy(self):
        response = self.client.get(self.settings_privacy_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_privacy.html")

    def test_user_settings_password(self):
        response = self.client.get(self.settings_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_password.html")

    def test_user_settings_error(self):
        response = self.client.get(self.settings_error_url)
        self.assertEqual(response.status_code, 302)

    def test_sigin_withUserLoggedIn(self):
        response = self.client.post(
            self.sigin_url,
            data={"sign-in": "", "username": "EashanKaushik", "password": "coviguard"},
        )
        self.assertEqual(response.status_code, 302)


class AtomicTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.hasher = PBKDF2WrappedSHA1PasswordHasher()

        self.user_profile_url = reverse("login:user_profile", args=["EashanKaushik"])

        self.user_profile_url_error = reverse("login:user_profile", args=[1])

        self.user_profile_url_error_2 = reverse(
            "login:user_profile", args=["ChinmayKulkarni"]
        )

        self.privacy_url = reverse("login:privacy", args=["EashanKaushik"])

        self.change_password_url = reverse(
            "login:change_password", args=["EashanKaushik"]
        )

        self.sigup_url = reverse(
            "login:signup",
        )

        self.userdata = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password=self.hasher.encode("coviguard", "test123"),
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.userdata2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password=self.hasher.encode("coviguard", "test123"),
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.privacy = Privacy.objects.create(
            username=self.userdata,
            show_vacination=True,
            show_people_met=True,
            show_location_visited=False,
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

        self.policy = Policy.objects.create(
            policy_id=1,
            policy_name="TestPolicy",
            policy_desc="TestPolicyDesc",
            policy_level=0,
        )

        self.compliance = CirclePolicyCompliance.objects.create(
            circle_id=self.circle,
            policy_id=self.policy,
            username=self.userdata,
            compliance=True,
        )

    def test_user_profile_post(self):
        with open(
            os.path.join(Path(__file__).parent.absolute(), "famliy.jpg"),
            "rb",
        ) as imgData:
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
                    "vaccination_status_no": "",
                    "user_image": imgData,
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

    def test_user_privacy_post(self):
        response = self.client.post(
            self.privacy_url,
            data={
                "submit_change": "",
                "vaccination_status_yes": True,
                "vaccination_status_no": False,
                "people_met_yes": True,
                "people_met_no": False,
                "locaiton_visited_yes": True,
                "locaiton_visited_no": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_privacy.html")

    def test_user_change_password_post(self):
        response = self.client.post(
            self.change_password_url,
            data={
                "submit_change": "",
                "old_password": "coviguard",
                "new_password": "coviguard",
                "confirm_password": "coviguard",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/user_password.html")

    def test_signup_post(self):
        response = self.client.post(
            self.sigup_url,
            data={
                "signup-button": "",
                "password": "coviguard",
                "confirmpassword": "coviguard",
                "firstname": "NewTestUser",
                "lastname": "TestLastName",
                "username": "TestUsername",
                "email": "test@gmail.com",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_signup_post_error(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.post(
            self.sigup_url,
            data={
                "signup-button": "",
                "password": "coviguard",
                "confirmpassword": "covi",
                "firstname": "NewTestUser",
                "lastname": "TestLastName",
                "username": "TestUsername",
                "email": "test@gmail.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/signup.html")

    def test_signup_post_error_2(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.post(
            self.sigup_url,
            data={
                "signup-button": "",
                "password": "Coviguard@123",
                "confirmpassword": "Coviguard@123",
                "firstname": "Eashan",
                "lastname": "TestLastName",
                "email": "test@gmail.com",
                "username": "EashanKaushik",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_post_error_3(self):
        del self.session["user_key"]
        self.session.save()
        response = self.client.post(
            self.sigup_url,
            data={
                "signup-button": "",
                "password": "Coviguard@123",
                "confirmpassword": "Coviguard@123",
                "firstname": "Eashan",
                "lastname": "TestLastName",
                "email": "test@gmail.com",
                "username": "NewTestUser3",
            },
        )
        self.assertEqual(response.status_code, 302)
