from django.test import TestCase, Client
from selftracking.models import SelfTrack
from django.urls import reverse
from login.models import UserData
from alert.models import Alert
from circle.models import CircleUser, Circle
from selftracking.driver import get_user_met, get_location_visited

import datetime
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.session = self.client.session

        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"

        self.session.save()

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

        self.userdata_2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.alert = Alert.objects.create(
            username=self.userdata,
        )

        self.selftrack_data = SelfTrack.objects.create(
            date_uploaded=datetime.datetime.now(),
            username=self.userdata,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=9,
            largest_streak=10,
        )

        self.SelfTrackData = SelfTrack.objects.create(
            date_uploaded=datetime.datetime.now(),
            username=self.userdata,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=9,
            largest_streak=10,
        )

        self.SelfTrackData_2 = SelfTrack.objects.create(
            date_uploaded=datetime.date.today() + datetime.timedelta(days=-2),
            username=self.userdata_2,
            user_met="42a7b2626eae970122e01f65af2f5092",
            location_visited="42a7b2626eae970122e01f65af2f5092",
            streak=0,
            largest_streak=0,
        )

        self.circle = Circle.objects.create(
            circle_id=1,
            circle_name="TestCircle",
            admin_username=self.userdata,
            no_of_users=2,
        )

        self.CircleUserData = CircleUser.objects.create(
            circle_id=self.circle,
            username=self.userdata,
            is_admin=True,
            is_member=True,
        )

        self.CircleUserData_2 = CircleUser.objects.create(
            circle_id=self.circle,
            username=self.userdata_2,
            is_admin=False,
            is_member=True,
        )

        self.selftrack_url = reverse(
            "selftracking:selftrack",
            args=["cs55"],
        )

        self.selftrack_url_real = reverse(
            "selftracking:selftrack",
            args=["EashanKaushik"],
        )

        self.selftrack_url_real_3 = reverse(
            "selftracking:selftrack",
            args=["ChinmayKulkarni"],
        )

        self.client2 = Client()

        self.session2 = self.client2.session

        self.session2["user_key"] = None

        self.session2.save()

        self.selftrack_url_real2 = reverse(
            "selftracking:selftrack",
            args=[None],
        )

    def test_add_self_track(self):
        response = self.client.get(self.selftrack_url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_add_self_track_real(self):
        response = self.client.get(self.selftrack_url_real)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_getself_track(self):
        # Issue a GET request.
        response = self.client.get("selftracking/self_track.html")
        # print(response)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")
        self.assertEqual(response.status_code, 404)

    def test_add_selftrack(self):

        response = self.client.post(
            {"username": "name", "user_met": "pass", "location_visited": "1225"}
        )

        self.assertNotEqual(response.status_code, 302)

    def test_selftrack_data(self):
        response = self.client.get(self.selftrack_url_real)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_user2_monitor(self):
        response = self.client2.get(self.selftrack_url_real2)
        self.assertEqual(response.status_code, 302)
        url = reverse("login:error")
        # print(response.url)
        # print(url)
        self.assertEqual(url, response.url)

    def test_add_self_track_post(self):
        self.session[
            "user_key"
        ] = "IkNoaW5tYXlLdWxrYXJuaSI:1noBht:abL7sx3IPJVuK_xzPy-EUdKZwwZS-Mih7xjpThi6NLA"
        self.session.save()
        response = self.client.post(
            self.selftrack_url_real_3,
            data={
                "track": "",
                "user_met": '["met1"]',
                "location_visited": '["location_visited"]',
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_add_self_track_uploadedYesterday(self):
        self.SelfTrackData_3 = SelfTrack.objects.create(
            date_uploaded=datetime.date.today() + datetime.timedelta(days=-1),
            username=self.userdata_2,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=0,
            largest_streak=0,
        )
        self.session[
            "user_key"
        ] = "IkNoaW5tYXlLdWxrYXJuaSI:1noBht:abL7sx3IPJVuK_xzPy-EUdKZwwZS-Mih7xjpThi6NLA"
        self.session.save()
        response = self.client.post(
            self.selftrack_url_real_3,
            data={
                "track": "",
                "user_met": '["met1"]',
                "location_visited": '["location_visited"]',
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_add_self_track_uploadedYesterday_2(self):
        self.SelfTrackData_3 = SelfTrack.objects.create(
            date_uploaded=datetime.date.today() + datetime.timedelta(days=-1),
            username=self.userdata_2,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=0,
            largest_streak=10,
        )
        self.session[
            "user_key"
        ] = "IkNoaW5tYXlLdWxrYXJuaSI:1noBht:abL7sx3IPJVuK_xzPy-EUdKZwwZS-Mih7xjpThi6NLA"
        self.session.save()
        response = self.client.post(
            self.selftrack_url_real_3,
            data={
                "track": "",
                "user_met": '["met1"]',
                "location_visited": '["location_visited"]',
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_add_self_track_update(self):
        self.SelfTrackData_3 = SelfTrack.objects.create(
            date_uploaded=datetime.date.today() + datetime.timedelta(days=0),
            username=self.userdata_2,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=0,
            largest_streak=10,
        )
        self.session[
            "user_key"
        ] = "IkNoaW5tYXlLdWxrYXJuaSI:1noBht:abL7sx3IPJVuK_xzPy-EUdKZwwZS-Mih7xjpThi6NLA"
        self.session.save()
        response = self.client.post(
            self.selftrack_url_real_3,
            data={
                "track-update": "",
                "user_met": '["met1"]',
                "location_visited": '["location_visited"]',
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_driver_code(self):
        self.userdata_3 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="TestUser",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        self.SelfTrackData_4 = SelfTrack.objects.create(
            date_uploaded=datetime.date.today() + datetime.timedelta(days=0),
            username=self.userdata_3,
            user_met=json.dumps(["met1"]),
            location_visited=json.dumps(["11225"]),
            streak=0,
            largest_streak=10,
        )
        get_user_met("TestUser")
        get_location_visited("TestUser")


class TestExceptionViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.session = self.client.session

        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"

        self.session.save()

        self.userdata = UserData.objects.create(
            firstname="new",
            lastname="user",
            password="coviguard",
            username="exceptionuser",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.alert = Alert.objects.create(
            username=self.userdata,
        )

        self.selftrack_url_exp = reverse(
            "selftracking:selftrack",
            args=["exceptionuser"],
        )

        self.selftrack_url_exp_2 = reverse(
            "selftracking:selftrack",
            args=["EashanKaushik"],
        )

        self.selftrack = SelfTrack()

    def test_add_self_track_exception(self):
        response = self.client.get(self.selftrack_url_exp)
        self.assertNotEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "selftracking/self_track.html")

    def test_new_user_exception(self):
        self.userdata_2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )
        response = self.client.get(self.selftrack_url_exp_2)
        self.assertEqual(response.status_code, 200)
