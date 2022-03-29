from django.db import models
from login.models import UserData

# Create your models here.
class SelfTrack(models.Model):
    date_uploaded = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    user_met = models.CharField(max_length=100)
    location_visited = models.CharField(max_length=100)
