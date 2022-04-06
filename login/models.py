from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random


def random_img():
    return "media/default/user/" + str(random.randint(1, 6)) + ".svg"


class UserData(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default="coviguard")
    username = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100, default="a@b.com")
    dob = models.DateField(null=True)
    phone = PhoneNumberField(null=True)
    work_address = models.CharField(max_length=200, null=True)
    home_adress = models.CharField(max_length=200, null=True)
    is_vacinated = models.BooleanField(default=False)
    user_image = models.ImageField(default=random_img, upload_to="media/user/")


class Privacy(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    show_vacination = models.BooleanField(default=False)
    show_people_met = models.BooleanField(default=False)
    show_location_visited = models.BooleanField(default=False)
