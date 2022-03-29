from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserData(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=50, default="coviguard")
    username = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100, default="a@b.com")
    dob = models.DateField(null=True)
    phone = PhoneNumberField(null=True)
    work_address = models.CharField(max_length=200, null=True)
    home_adress = models.CharField(max_length=200, null=True)
    is_vacinated = models.BooleanField(default=False)
