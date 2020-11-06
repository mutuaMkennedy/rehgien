"""
    <---How pros are added--->
        Pros create an account and are added as normal users then they make a request to have their
        account updgraded to pro. We take the request verify it and add their account
        to a pro category
    <---How pros are stored--->
        A pro is saved in a pro category predefined by rehgien
        then they can select their speciality from the list availlable to them and
        lastryle specify their services
    <---To do--->
        merge pro tables to one table with a field for specifying pro business listing
        category, area of speciality and services.
"""
#Speciality field represents field of expertise for the pro

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from django.contrib.gis.db import models
from django.db.models import Avg
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from cloudinary.models import CloudinaryField
import sys
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import cloudinary
from embed_video.fields import EmbedVideoField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


# extending user model
class User(AbstractUser):
    user_type_choices = (
                ('NormalUser','NormalUser'),
                ('Agent','Agent'),
                ('PropertyManager','PropertyManager'),
                ('Design&servicePro','Design&servicePro'),
                ('Company', 'Company'),
                ('Admin','Admin')
                )

    user_type = models.CharField(max_length=20,choices=user_type_choices, default='NormalUser')
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)

    @property
    def percentage_complete(self):
        percent = { 'username': 10, 'first_name': 25, 'last_name': 25, 'email': 10, 'profile_image': 30}
        total = 0
        if self.username:
            total += percent.get('username', 0)
        if self.first_name:
            total += percent.get('first_name', 0)
        if self.last_name:
            total += percent.get('last_name', 0)
        if self.email:
            total += percent.get('email', 0)
        if self.profile_image:
            total += percent.get('profile_image', 0)
        return "%s"%(total)

#Professional model tables from here

class CompanyProfile(models.Model):
    speciality_choices = (
    ('Property Management', 'Property Management'),
    ('Agency', 'Agency'),
    ('Consultancy', 'Consultancy')
    )
    account_type_choices = (
        ('Basic', 'Basic'),
        ('Premium Agent','Premium Agent'),
        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = None, related_name = 'company_profile')
    banner_image = models.ImageField(upload_to = 'banner_images/', blank = True)
    speciality = MultiSelectField(choices = speciality_choices, default = 'Property Management', max_length=100)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'agent_profile')
    service_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'company_saves', blank = True)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'company_followers', blank = True)
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    featured_business = models.BooleanField(default=False, null=True, blank=True)

    @property
    def percentage_complete(self):
        percent = {
        'banner_image': 10, 'speciality':10, 'phone':10, 'license_number':10, 'address':10, 'website_link':5,
        'facebook_link': 5, 'twitter_link': 5, 'linkedin_link':5, 'location':10, 'about':20
        }
        total = 0
        if self.banner_image:
            total += percent.get('banner_image', 0)
        if self.speciality:
            total += percent.get('speciality', 0)
        if self.phone:
            total += percent.get('phone', 0)
        if self.license_number:
            total += percent.get('license_number', 0)
        if self.address:
            total += percent.get('address', 0)
        if self.website_link:
            total += percent.get('website_link', 0)
        if self.facebook_link:
            total += percent.get('facebook_link', 0)
        if self.twitter_link:
            total += percent.get('twitter_link', 0)
        if self.linkedin_link:
            total += percent.get('linkedin_link', 0)
        if self.location:
            total += percent.get('location', 0)
        if self.about:
            total += percent.get('about', 0)
        return "%s"%(total)

    @property
    def longitude(self):
    	return self.location.x

    @property
    def latitude(self):
    	return self.location.y

    def get_absolute_url(self):
        return reverse( 'profiles:business_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'CompanyProfiles'

    @property
    def average_rating(self):
        return self.company_review.all().aggregate(Avg('rating')).get('rating__avg', 0.00)

class CompanyTopClient(models.Model):
    profile = models.ForeignKey(CompanyProfile, related_name = 'co_top_clients', on_delete = models.CASCADE)
    client_logo = CloudinaryField('image', blank=False, overwrite=True, resource_type='image',
	 						folder='client_logos')
    client_name = models.CharField(max_length = 25, blank=False)
    business_category = models.CharField(max_length = 25, blank=False)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return  self.client_name + ' - ' + self.business_category

    class Meta:
        verbose_name_plural = "CompanyTopClients"

class CompanyBusinessHours(models.Model):
    WEEKDAYS = [
      (1, _("Monday")),
      (2, _("Tuesday")),
      (3, _("Wednesday")),
      (4, _("Thursday")),
      (5, _("Friday")),
      (6, _("Saturday")),
      (7, _("Sunday")),
    ]
    user = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='co_business_hours', blank=True, null=True)
    weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        verbose_name_plural = 'CompanyBusinessHours'
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                self.from_hour, self.to_hour)

class CompanyReviews(models.Model):
    rating_choices = (
        (1, 'Never'),(2, 'Not likely'),
        (3, 'Mybe'),(4, 'Likely'),
        (5, 'Highly likely'),
        )
    responsive_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    knowledge_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    negotiation_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    professionalism_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    service_choices = (
        ('1', 'Helped me sell my home.'),('2', 'Helped me find tenants.'),
        ('3', 'Helped me buy a home.'),('4', 'Helped me find a rental.'),
        ('5', 'Consultation.'),('6', 'Listed my property on Rehgien.'),
        ('7', 'None. Reached out but never responded.'),('8', 'Managed(s) my property.'),
    )
    profile = models.ForeignKey(CompanyProfile, related_name='company_review', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=rating_choices, null=True)
    responsive_rating = models.PositiveIntegerField(choices=responsive_rating_choices, null=True)
    knowledge_rating = models.PositiveIntegerField(choices=knowledge_rating_choices, null=True)
    negotiation_rating = models.PositiveIntegerField(choices=negotiation_rating_choices, null=True)
    professionalism_rating = models.PositiveIntegerField(choices=professionalism_rating_choices, null=True)
    service = models.CharField(choices=service_choices, max_length=50, null=True)
    comment = models.TextField(null=True)
    date_of_service = models.DateField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='review_company', on_delete=models.CASCADE, null=True)
    review_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  'User ID: ' + str(self.profile.user.pk) + ' - ' + self.profile.user.email + ' - ' + 'Rated: '+ str(self.rating)

    class Meta:
        verbose_name_plural = 'CompanyReviews'

# Estate Agent Profile
class AgentProfile(models.Model):
    speciality_choices = (
        ('1', 'Buying and Selling of houses'),
        ('2', 'Renting houses'),
        ('3', 'Leasing office spaces'),
        ('4', 'Buying and selling of land'),
        )
    account_type_choices = (
        ('Basic', 'Basic'),
        ('Premium Agent','Premium Agent'),
        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = None, related_name = 'agent_profile')
    banner_image = models.ImageField(upload_to = 'banner_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    speciality = MultiSelectField(null=True, blank=True, choices=speciality_choices, default='1')
    about = RichTextField(blank=True, config_name = 'agent_profile', null=True)
    service_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)

    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'agent_saves', blank = True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'agent_followers', blank = True)
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    featured_agent = models.BooleanField(default=False, null=True, blank=True)

    @property
    def percentage_complete(self):
        percent = {
        'banner_image': 10, 'speciality':10, 'phone':10, 'license_number':10, 'address':10, 'website_link':5,
        'facebook_link': 5, 'twitter_link': 5, 'linkedin_link':5, 'location':10, 'about':20
        }
        total = 0
        if self.banner_image:
            total += percent.get('banner_image', 0)
        if self.speciality:
            total += percent.get('speciality', 0)
        if self.phone:
            total += percent.get('phone', 0)
        if self.license_number:
            total += percent.get('license_number', 0)
        if self.address:
            total += percent.get('address', 0)
        if self.website_link:
            total += percent.get('website_link', 0)
        if self.facebook_link:
            total += percent.get('facebook_link', 0)
        if self.twitter_link:
            total += percent.get('twitter_link', 0)
        if self.linkedin_link:
            total += percent.get('linkedin_link', 0)
        if self.location:
            total += percent.get('location', 0)
        if self.about:
            total += percent.get('about', 0)
        return "%s"%(total)

    @property
    def longitude(self):
    	return self.location.x

    @property
    def latitude(self):
    	return self.location.y

    def get_absolute_url(self):
        return reverse( 'profiles:agent_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.first_name + \
         '-' + self.user.last_name + '-' + self.user.email + '-' + self.phone

    class Meta:
        verbose_name_plural = 'AgentProfiles'

    @property
    def average_rating(self):
        return self.agent_review.all().aggregate(Avg('rating')).get('rating__avg', 0.00)

class AgentTopClient(models.Model):
    profile = models.ForeignKey(AgentProfile, related_name = 'ag_top_clients', on_delete = models.CASCADE)
    client_logo = CloudinaryField('image', blank=False, overwrite=True, resource_type='image',
	 						folder='client_logos')
    client_name = models.CharField(max_length = 25, blank=False)
    business_category = models.CharField(max_length = 25, blank=False)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return  self.client_name + ' - ' + self.business_category

    class Meta:
        verbose_name_plural = "AgentTopClients"

class AgentBusinessHours(models.Model):
    WEEKDAYS = [
      (1, _("Monday")),
      (2, _("Tuesday")),
      (3, _("Wednesday")),
      (4, _("Thursday")),
      (5, _("Friday")),
      (6, _("Saturday")),
      (7, _("Sunday")),
    ]
    user = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='ag_business_hours', blank=True, null=True)
    weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        verbose_name_plural = 'AgentBusinessHours'
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                self.from_hour, self.to_hour)

class AgentReviews(models.Model):
    rating_choices = (
        (1, 'Never'),(2, 'Not likely'),
        (3, 'Mybe'),(4, 'Likely'),
        (5, 'Highly likely'),
        )
    responsive_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    knowledge_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    negotiation_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    professionalism_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    service_choices = (
        ('1', 'Helped me sell my home.'),('2', 'Helped me find tenants.'),
        ('3', 'Helped me buy a home.'),('4', 'Helped me find a rental.'),
        ('5', 'Consultation.'),('6', 'Listed my property on Rehgien.'),
        ('7', 'None. Reached out but agent never responded.'),('8', 'Managed(s) my property.'),
    )
    profile = models.ForeignKey(AgentProfile, related_name='agent_review', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=rating_choices, null=True)
    responsive_rating = models.PositiveIntegerField(choices=responsive_rating_choices, null=True)
    knowledge_rating = models.PositiveIntegerField(choices=knowledge_rating_choices, null=True)
    negotiation_rating = models.PositiveIntegerField(choices=negotiation_rating_choices, null=True)
    professionalism_rating = models.PositiveIntegerField(choices=professionalism_rating_choices, null=True)
    service = models.CharField(choices=service_choices, max_length=50, null=True)
    comment = models.TextField(null=True)
    date_of_service = models.DateField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='review_user', on_delete=models.CASCADE, null=True)
    review_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  'User ID: ' + str(self.profile.user.pk) + ' - ' + self.profile.user.email + ' - ' + 'Rated: '+ str(self.rating)

    class Meta:
        verbose_name_plural = 'AgentReviews'

# Property managers
class PropertyManagerProfile(models.Model):
    account_type_choices = (
        ('Basic', 'Basic'),
        ('Premium Manager','Premium Manager'),
        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = None, related_name = 'pm_profile')
    banner_image = models.ImageField(upload_to = 'banner_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'agent_profile')
    service_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)

    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'pm_saves', blank = True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'pm_followers', blank = True)
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    featured_agent = models.BooleanField(default=False, null=True, blank=True)

    @property
    def percentage_complete(self):
        percent = {
        'banner_image': 10, 'phone':10, 'license_number':15, 'address':15, 'website_link':5,
        'facebook_link': 5, 'twitter_link': 5, 'linkedin_link':5, 'location':10, 'about':20
        }
        total = 0
        if self.banner_image:
            total += percent.get('banner_image', 0)
        if self.phone:
            total += percent.get('phone', 0)
        if self.license_number:
            total += percent.get('license_number', 0)
        if self.address:
            total += percent.get('address', 0)
        if self.website_link:
            total += percent.get('website_link', 0)
        if self.facebook_link:
            total += percent.get('facebook_link', 0)
        if self.twitter_link:
            total += percent.get('twitter_link', 0)
        if self.linkedin_link:
            total += percent.get('linkedin_link', 0)
        if self.location:
            total += percent.get('location', 0)
        if self.about:
            total += percent.get('about', 0)
        return "%s"%(total)

    @property
    def longitude(self):
    	return self.location.x

    @property
    def latitude(self):
    	return self.location.y

    def get_absolute_url(self):
        return reverse( 'profiles:pm_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.first_name + \
         '-' + self.user.last_name + '-' + self.user.email + '-' + self.phone

    class Meta:
        verbose_name_plural = 'PropertyManagerProfiles'

    @property
    def average_rating(self):
        return self.pm_review.all().aggregate(Avg('rating')).get('rating__avg', 0.00)

class PropertyManagerTopClient(models.Model):
    profile = models.ForeignKey(PropertyManagerProfile, related_name = 'pm_top_clients', on_delete = models.CASCADE)
    client_logo = CloudinaryField('image', blank=False, overwrite=True, resource_type='image',
	 						folder='client_logos')
    client_name = models.CharField(max_length = 25, blank=False)
    business_category = models.CharField(max_length = 25, blank=False)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return  self.client_name + ' - ' + self.business_category

    class Meta:
        verbose_name_plural = "PropertyManagerTopClients"

class PropertyManagerBusinessHours(models.Model):
    WEEKDAYS = [
      (1, _("Monday")),
      (2, _("Tuesday")),
      (3, _("Wednesday")),
      (4, _("Thursday")),
      (5, _("Friday")),
      (6, _("Saturday")),
      (7, _("Sunday")),
    ]
    user = models.ForeignKey(PropertyManagerProfile, on_delete=models.CASCADE, related_name='pm_business_hours', blank=True, null=True)
    weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        verbose_name_plural = 'PropertyManagerBusinessHours'
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                self.from_hour, self.to_hour)

class PropertyManagerReviews(models.Model):
    rating_choices = (
        (1, 'Never'),(2, 'Not likely'),
        (3, 'Mybe'),(4, 'Likely'),
        (5, 'Highly likely'),
        )
    responsive_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    communication_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    attention_to_detail_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    service_choices = (
        ('1', 'Helped me find tenants.'),('2', 'Helped me find a rental.'),
        ('3', 'Consultation.'),('4', 'Listed my property on Rehgien.'),
        ('5', 'None. Reached out but agent never responded.'),('6', 'Managed(s) my property.'),
        ('7', 'Other real estate service.'),
    )
    profile = models.ForeignKey(PropertyManagerProfile, related_name='pm_review', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=rating_choices, null=True)
    responsive_rating = models.PositiveIntegerField(choices=responsive_rating_choices, null=True)
    communication_rating = models.PositiveIntegerField(choices=communication_rating_choices, null=True)
    attention_to_detail = models.PositiveIntegerField(choices=attention_to_detail_choices, null=True)
    service = models.CharField(choices=service_choices, max_length=50, null=True)
    comment = models.TextField(null=True)
    date_of_service = models.DateField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pm_review_user', on_delete=models.CASCADE, null=True)
    review_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  'User ID: ' + str(self.profile.user.pk) + ' - ' + self.profile.user.email + ' - ' + 'Rated: '+ str(self.rating)

    class Meta:
        verbose_name_plural = 'PropertyManagerReviews'

# Design and services
class DesignAndServiceProProfile(models.Model):
    account_type_choices = (
        ('Basic', 'Basic'),
        ('Premium account','Premium account'),
        )
    pro_speciality = (
        ('Interior Designer', 'Interior Designer'),
        ('Architect','Architect'),
        ('Landscape architect','Landscape architect'),
        ('Home mover','Home mover'),
        ('Plumbing','Plumbing'),
        ('Photographer','Photographer'),
        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = None, related_name = 'DService_profile')
    banner_image = models.ImageField(upload_to = 'banner_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'agent_profile')
    service_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)

    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'ds_saves', blank = True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'ds_followers', blank = True)
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    pro_speciality = models.CharField(max_length=20, choices=pro_speciality,blank = True , null=True)
    featured_pro = models.BooleanField(default=False, null=True, blank=True)

    @property
    def percentage_complete(self):
        percent = {
        'banner_image': 10, 'pro_speciality':15, 'phone':10, 'address':10, 'website_link':5,
        'facebook_link': 5, 'twitter_link': 5,'instagram_link':5, 'linkedin_link':5, 'location':10, 'about':20
        }
        total = 0
        if self.banner_image:
            total += percent.get('banner_image', 0)
        if self.pro_speciality:
            total += percent.get('pro_speciality', 0)
        if self.phone:
            total += percent.get('phone', 0)
        if self.instagram_link:
            total += percent.get('instagram_link', 0)
        if self.address:
            total += percent.get('address', 0)
        if self.website_link:
            total += percent.get('website_link', 0)
        if self.facebook_link:
            total += percent.get('facebook_link', 0)
        if self.twitter_link:
            total += percent.get('twitter_link', 0)
        if self.linkedin_link:
            total += percent.get('linkedin_link', 0)
        if self.location:
            total += percent.get('location', 0)
        if self.about:
            total += percent.get('about', 0)
        return "%s"%(total)

    @property
    def longitude(self):
    	return self.location.x

    @property
    def latitude(self):
    	return self.location.y

    def get_absolute_url(self):
        return reverse( 'profiles:d_service_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.first_name + \
         '-' + self.user.last_name + '-' + self.user.email + '-' + self.phone

    class Meta:
        verbose_name_plural = 'DesignAndServiceProProfiles'

    @property
    def average_rating(self):
        return self.DService_review.all().aggregate(Avg('rating')).get('rating__avg', 0.00)

class DSTopClient(models.Model):
    profile = models.ForeignKey(DesignAndServiceProProfile, related_name = 'ds_top_clients', on_delete = models.CASCADE)
    client_logo = CloudinaryField('image', blank=False, overwrite=True, resource_type='image',
	 						folder='client_logos')
    client_name = models.CharField(max_length = 25, blank=False)
    business_category = models.CharField(max_length = 25, blank=False)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return  self.client_name + ' - ' + self.business_category

    class Meta:
        verbose_name_plural = "DSTopClients"

class DSBusinessHours(models.Model):
    WEEKDAYS = [
      (1, _("Monday")),
      (2, _("Tuesday")),
      (3, _("Wednesday")),
      (4, _("Thursday")),
      (5, _("Friday")),
      (6, _("Saturday")),
      (7, _("Sunday")),
    ]
    user = models.ForeignKey(DesignAndServiceProProfile, on_delete=models.CASCADE, related_name='DS_business_hours', blank=True, null=True)
    weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        verbose_name_plural = 'DSBusinessHours'
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                self.from_hour, self.to_hour)

class DesignAndServiceProReviews(models.Model):
    rating_choices = (
        (1, 'Never'),(2, 'Not likely'),
        (3, 'Mybe'),(4, 'Likely'),
        (5, 'Highly likely'),
        )
    quality_rating_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    creativity_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    attention_to_detail_choices = (
    (1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
    (4, 'Good'),(5, 'Very good'),
    )
    profile = models.ForeignKey(DesignAndServiceProProfile, related_name='DService_review', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=rating_choices, null=True)
    quality_rating = models.PositiveIntegerField(choices=quality_rating_choices, null=True)
    creativity_rating = models.PositiveIntegerField(choices=creativity_choices, null=True)
    attention_to_detail = models.PositiveIntegerField(choices=attention_to_detail_choices, null=True)
    comment = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DService_review_user', on_delete=models.CASCADE, null=True)
    review_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return  'User ID: ' + str(self.profile.user.pk) + ' - ' + self.profile.user.email + ' - ' + 'Rated: '+ str(self.rating)

    class Meta:
        verbose_name_plural = 'DesignAndServiceProReviews'

#Pro projects and portfolios
class  PMPortfolio(models.Model):
    current_manager_choices = (
    ('Yes', 'Yes'),
    ('No', 'No')
    )
    property_name = models.CharField(max_length = 50, blank = False, null = True)
    property_market_value = models.PositiveIntegerField(blank= False, null = True)
    property_location = models.CharField(max_length = 200, blank = False, null = True)
    property_map_point = models.PointField(srid=4326, null=True)
    currently_managing = models.CharField(max_length = 3,default='Yes',choices = current_manager_choices, blank = False, null = True)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default = None, related_name = 'PM_portfolio_ls_creator', on_delete = models.CASCADE)

    @property
    def longitude(self):
        return self.property_name.x

    @property
    def latitude(self):
        return self.property_name.y

    def __str__(self):
        return self.created_by.username + '-' + self.property_name + '-' + self.property_location + '-' + str(self.property_market_value)

    class Meta:
        verbose_name_plural = 'PMPortfolio'

class PMPortfolioImages(models.Model):
    portfolio = models.ForeignKey(PMPortfolio, related_name = "PM_porfolio_Images", on_delete = models.CASCADE)
    property_image = CloudinaryField('image', blank=True, overwrite=True, resource_type='image',
	 						folder='PM_porfolio_photos')

    def save(self, *args, **kwargs):
        if not self.id:
            self.property_image = self.compressImage(self.property_image)
        super(PMPortfolioImages,   self).save(*args,   **kwargs)

    def compressImage(self,image):
        imageTemporary	=	Image.open(image)
        outputIoStream	=	BytesIO()
        imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
        imageTemporary.save(outputIoStream , format='JPEG', quality=70) # change quality according to requirement.
        outputIoStream.seek(0)
        uploadedImage	=	InMemoryUploadedFile(outputIoStream,'CloudinaryField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

@receiver(pre_delete, sender=PMPortfolioImages)
def PM_photo_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.property_image.public_id)

class  DesignAndServiceProProjects(models.Model):
    project_name = models.CharField(max_length = 50, blank = False, null = True)
    project_cost = models.PositiveIntegerField(blank = False, null = True)
    project_description = models.TextField(blank = False, null = True)
    project_video = EmbedVideoField(blank = True, null = True)
    project_location = models.CharField(max_length = 200, blank = False, null = True)
    project_map_point = models.PointField(srid=4326, null=True)
    project_year = models.CharField(max_length = 4, blank = False, null = True,validators=[RegexValidator(r'^\d{1,10}$')])
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default = None, related_name = 'DS_project_ls_creator', on_delete = models.CASCADE)

    @property
    def longitude(self):
        return self.project_map_point.x

    @property
    def latitude(self):
        return self.project_map_point.y

    def __str__(self):
        return self.created_by.username + '-' + self.project_name + '-' + self.project_location

    class Meta:
        verbose_name_plural = 'DesignAndServiceProProjects'

class DSProProjectImages(models.Model):
    project = models.ForeignKey(DesignAndServiceProProjects, related_name = "DS_project_Images", on_delete = models.CASCADE)
    project_image = CloudinaryField('image', blank=True, overwrite=True, resource_type='image',
	 						folder='DS_project_photos')

    def save(self, *args, **kwargs):
        if not self.id:
            self.project_image = self.compressImage(self.project_image)
        super(DSProProjectImages,   self).save(*args,   **kwargs)

    def compressImage(self,image):
        imageTemporary	=	Image.open(image)
        outputIoStream	=	BytesIO()
        imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
        imageTemporary.save(outputIoStream , format='JPEG', quality=70) # change quality according to requirement.
        outputIoStream.seek(0)
        uploadedImage	=	InMemoryUploadedFile(outputIoStream,'CloudinaryField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

@receiver(pre_delete, sender=DSProProjectImages)
def DS_photo_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.project_image.public_id)

#professional teammates
class TeammateConnection(models.Model):
    accepted_choices = (
    ('Yes', 'Yes'),
    ('No' , 'No')
    )
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'join_team_requestor', on_delete = models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'join_team_request_receiver', on_delete = models.CASCADE)
    receiver_accepted = models.CharField(choices = accepted_choices, default = 'No', max_length = 3, blank = True, null=True)
    starred = models.BooleanField(default = False, blank=True, null=True)

    def __str__(self):
        return str(self.requestor) + " - " + str(self.receiver) + " - " + self.receiver_accepted
