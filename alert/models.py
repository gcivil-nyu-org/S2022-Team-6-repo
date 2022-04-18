from django.db import models
from login.models import UserData

# Create your models here.


class Alert(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    location_data_case = models.TextField(null=True)
    location_data_death = models.TextField(null=True)
    location_alert_case = models.BooleanField(default=False)
    location_alert_death = models.BooleanField(default=False)
    home_alert_case = models.BooleanField(default=False)
    home_alert_death = models.BooleanField(default=False)
    work_alert_case = models.BooleanField(default=False)
    work_alert_death = models.BooleanField(default=False)
    people_data = models.TextField(null=True)
    people_alert = models.BooleanField(default=False)
    alert = models.BooleanField(default=False)


class AlertNotification(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    notification = models.CharField(max_length=300)
    updated = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    alert_for = models.CharField(max_length=300, null=True)
