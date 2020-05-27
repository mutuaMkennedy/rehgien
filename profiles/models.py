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
# Create your models here.

# extending user model
class User(AbstractUser):
    user_type_choices = (
                ('NormalUser','Normaluser'),
                ('Agent','Agent'),
                ('PropertyManager','PropertyManager'),
                ('Design&servicePro','Design&servicePro'),
                ('Admin','Admin')
                )

    user_type = models.CharField(max_length=10,choices=user_type_choices, default='NormalUser')

# Extra data on users through profiles from here
#Default profile for normal users
class NormalUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = None, related_name = 'n_user_profile')
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)

    # def get_absolute_url(self):
    #     return reverse( 'profiles:agent_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.first_name + \
         '-' + self.user.last_name + '-' + self.user.email

    class Meta:
        verbose_name_plural = 'NormalUserProfiles'

def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = NormalUserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)

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
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True)
    speciality = MultiSelectField(null=True, blank=True, choices=speciality_choices, default='1')
    about = RichTextField(blank=True, config_name = 'agent_profile')
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    featured_agent = models.BooleanField(default=False, null=True, blank=True)

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
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True)
    license_number = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'agent_profile')
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    featured_agent = models.BooleanField(default=False, null=True, blank=True)

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
    profile_image = models.ImageField(upload_to = 'profile_images/', blank = True)
    phone = models.CharField(max_length=13, blank = True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    location = models.PointField(srid=4326, null=True)
    about = RichTextField(blank=True, config_name = 'agent_profile')
    member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='Basic')
    pro_speciality = models.CharField(max_length=20, choices=pro_speciality,blank = True , null=True)
    featured_pro = models.BooleanField(default=False, null=True, blank=True)

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
