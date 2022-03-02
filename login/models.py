from django.db import models

# Create your models here.


class UserData(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100, default='a@b.com')
    dob = models.DateField()
    phone = models.IntegerField(default=9999999999)
    work_address = models.CharField(max_length=200)
    home_adress = models.CharField(max_length=200)
    is_vacinated = models.BooleanField(default=False)
