from django.contrib import admin
from .models import Alert, AlertNotification

admin.site.register(Alert)
admin.site.register(AlertNotification)
