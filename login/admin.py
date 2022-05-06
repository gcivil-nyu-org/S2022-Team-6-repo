from django.contrib import admin

from .models import UserData, Privacy, Counties

admin.site.register(UserData)
admin.site.register(Privacy)
admin.site.register(Counties)
