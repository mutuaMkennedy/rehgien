from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from django.contrib.gis.db import models
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = None, related_name = 'profile')
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'user_profile')
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type_choices = (
    ('Basic', 'Basic'),
    ('Agent','Agent'),
    ('Poperty Manager', 'Property Manager'),
    ('Appraiser','Appraiser'),
    )
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Agent')

    def get_absolute_url(self):
        return reverse( 'profiles:account', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.first_name + '-' + self.user.last_name + '-' + self.user.email + '-' + self.phone

    class Meta:
        verbose_name_plural = 'UserProfiles'

    def get_absolute_url(self):
        return reverse( 'profiles:account', kwargs={'pk':self.pk} )

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)
