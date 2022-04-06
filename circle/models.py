from django.db import models
from login.models import UserData
import random

# Create your models here.


def random_img():
    return "media/default/circle/" + str(random.randint(1, 5)) + ".jpg"


class Circle(models.Model):
    circle_id = models.AutoField(primary_key=True)
    circle_name = models.CharField(max_length=100)
    admin_username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    no_of_users = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    group_image = models.ImageField(
        default=random_img, upload_to="media/circle/", null=True, blank=True
    )


class CircleUser(models.Model):
    class Meta:
        unique_together = (("circle_id", "username"),)

    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    # display_name = models.CharField(max_length=100)


class Policy(models.Model):
    policy_id = models.IntegerField(default=0, primary_key=True)
    policy_name = models.CharField(max_length=20)
    policy_desc = models.CharField(max_length=1000)
    policy_level = models.IntegerField(default=0)


class CirclePolicy(models.Model):
    class Meta:
        unique_together = (("circle_id", "policy_id"),)

    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)


class RequestCircle(models.Model):
    class Meta:
        unique_together = (("circle_id", "username"),)

    request_id = models.AutoField(primary_key=True)
    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)


class RecentCircle(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    recent_circle = models.TextField(null=True)


class CirclePolicyCompliance(models.Model):
    class Meta:
        unique_together = (("circle_id", "policy_id", "username"),)

    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)

    compliance = models.BooleanField(default=False)
