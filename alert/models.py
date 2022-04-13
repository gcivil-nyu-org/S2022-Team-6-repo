from django.db import models
from login.models import UserData

# Create your models here.


class Alert(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    alert = models.BooleanField(default=False)
