from django.contrib import admin
from . import models

class SupportedAppVersionAdmin(admin.ModelAdmin):
    list_display = (
    "app_type","platform","upgrade_type","app_version",
    )

admin.site.register(models.DeviceInformation)
admin.site.register(models.SupportedAppVersion,SupportedAppVersionAdmin)