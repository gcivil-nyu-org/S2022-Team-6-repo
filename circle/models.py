from django.db import models
from login.models import UserData
# Create your models here.


class Circle(models.Model):
    circle_id = models.AutoField(primary_key=True)
    circle_name = models.CharField(max_length=100)
    admin_username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    # admin_id = models.CharField(max_length=100, default=0)
    no_of_users = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    pending_request = models.IntegerField(default=0)
    #circle_display_image = models.ImageField(upload_to = 'images/')
    # description = models.TextField(null=True, blank=True)

    #def __str__(self):
    #    return str(self.admin_username)


class CircleUser(models.Model):
    class Meta:
        unique_together = (('circle_id', 'username'),)
    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)


class Policy(models.Model):
    policy_id = models.IntegerField(default=0, primary_key=True)
    policy_name = models.CharField(max_length=20)
    policy_desc = models.CharField(max_length=1000)
    policy_level = models.IntegerField(default=0)


class CirclePolicy(models.Model):
    class Meta:
        unique_together = (('circle_id', 'policy_id'),)
    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)


class RequestCircle(models.Model):
    class Meta:
        unique_together = (('circle_id', 'username'),)
    request_id = models.AutoField(primary_key=True)
    circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
