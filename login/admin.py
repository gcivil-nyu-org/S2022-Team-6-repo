from django.contrib import admin

# Register your models here.
from .models import UserData, Privacy

admin.site.register(UserData)
admin.site.register(Privacy)
