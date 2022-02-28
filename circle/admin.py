from django.contrib import admin
from .models import Circle, CircleUsers, CirclePolicies, Policy
# Register your models here.
admin.site.register(Circle)
admin.site.register(CircleUsers)
admin.site.register(CirclePolicies)
admin.site.register(Policy)