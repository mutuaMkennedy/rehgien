from django.db import models
from django.conf import settings
from notifications.base.models import AbstractNotification


# class Notification(AbstractNotification):
    # custom fields will go here

    # class Meta(AbstractNotification.Meta):
    #     abstract = False

class DeviceInformation(models.Model):
    device_type = (
        ('ANDROID','android'),
        ('APPLE','apple')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_device', on_delete=models.SET_NULL, default=None, null=True)
    type = models.CharField(choices=device_type, default=None, max_length=100)
    name = models.CharField(max_length=250,null=True)
    active = models.BooleanField(default=False)
    device_id =  models.UUIDField(default = None, null = True)
    expo_token = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name
