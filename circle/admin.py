from django.contrib import admin
from .models import (
    Circle,
    CircleUser,
    CirclePolicy,
    Policy,
    RequestCircle,
    RecentCircle,
)

# Register your models here.
admin.site.register(Circle)
admin.site.register(CircleUser)
admin.site.register(CirclePolicy)
admin.site.register(Policy)
admin.site.register(RequestCircle)
admin.site.register(RecentCircle)
