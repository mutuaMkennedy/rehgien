from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = None, related_name = 'profile')
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    email = models.EmailField(blank = True)
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)

    def get_absolute_url(self):
        return reverse( 'profiles:account', kwargs={'pk':self.pk})

    def __str__(self):
        return self.first_name + '-' + self.last_name + '-' + self.email + '-' + self.phone

    class Meta:
        verbose_name_plural = 'UserProfiles'

    def get_absolute_url(self):
        return reverse( 'profiles:account', kwargs={'pk':self.pk} )
