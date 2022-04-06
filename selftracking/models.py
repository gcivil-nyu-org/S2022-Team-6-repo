from django.db import models
from login.models import UserData
from django.utils.timezone import now


# Create your models here.
class SelfTrack(models.Model):
    date_uploaded = models.DateTimeField(default=now, editable=False)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    user_met = models.CharField(max_length=100)
    location_visited = models.CharField(max_length=100)
    streak = models.IntegerField(default=0)
    largest_streak = models.IntegerField(default=0)
