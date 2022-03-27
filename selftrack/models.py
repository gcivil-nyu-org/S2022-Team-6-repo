from django.db import models

# Create your models here.


class Selftrack(models.Model):
    username = models.CharField(max_length=100)
    usermet = models.CharField(max_length=100)
    locationgone = models.CharField(max_length=100)