"""
	<---How pros are added--->
		Pros create an account and are added as client users then they make a request to have their
		account updgraded to pro. We take the request verify heir credentials and add upgrade their account
		to pro
	<---How pros are stored--->
		A pro is saved in a pro category predefined by rehgien
		then they can select their speciality from the list availlable to them and
		lastryle specify their services
"""
#Speciality field represents field of expertise for the pro

from tabnanny import verbose
from django.db import models
from location import models as location_models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from django.contrib.gis.db import models
from django.db.models import Avg
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
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
from phonenumber_field.modelfields import PhoneNumberField
from contact import views as contact_views
from . import tasks as profile_celery_tasks
import datetime
from django.db.models import Func

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'

def current_year():
	return datetime.date.today().year

def max_value_current_year(value):
	return MaxValueValidator(current_year())(value)

# extending user model
class User(AbstractUser):
	user_type_choices = (
				('CLIENT','client'),
				('PRO','pro')
				)

	account_type_choices = (
		('BASIC', 'basic'),
		('PREMIUM','premium'),
		)

	user_type = models.CharField(max_length=20,choices=user_type_choices, default='CLIENT')
	profile_image = CloudinaryField('image', blank=True, null=True, overwrite=True, resource_type='image',
							folder='user_profile_photos')
	phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+254xxxxxxxxx'. Up to 14 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, null=True)
	account_type = models.CharField(max_length=10, choices=account_type_choices, default='BASIC')
	# Azure credentials for use in chat service
	azure_identity = models.TextField(blank=True, null=True)
	azure_access_token = models.TextField(blank=True, null=True)
	azure_token_expires_on = models.DateTimeField(blank=True, null=True, auto_now = False, auto_now_add = False)

	@property
	def percentage_complete(self):
		percent = { 'username': 10, 'first_name': 15, 'last_name': 15, 'email': 20,
		'profile_image': 30, 'user_type':5,'account_type':5}
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

# @receiver(pre_save, sender=User)
# def generate_custom_username(sender, instance, **kwargs):
# 	# check user has not provided a username
# 	if not instance.username:
# 		if instance.email:
# 			""" Use email to generate username if user has provided an email address"""
# 			user_email = instance.email
# 			# ensure characters dont exceed the max length of usernames in django
# 			username = user_email[:30]
# 			n = 1
# 			while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
# 				""" If there are existing usernames add a number at the end"""
# 				n += 1
# 				username = user_email[:(29 - len(str(n)))] + '-' + str(n)
# 			instance.username = username
# 		elif instance.phone:
# 			""" Use phone to generate username if user has not provided an email adress"""
# 			user_phone = instance.phone
# 			# ensure characters dont exceed the max length of usernames in django
# 			username = user_phone[:30]
# 			n = 1
# 			while User.objects.exclude(pk=instance.pk).filter(username=user_phone).exists():
# 				""" If there are existing usernames add a number at the end"""
# 				n += 1
# 				username = user_phone[:(29 - len(str(n)))] + '-' + str(n)
# 			instance.username = username		


class UserAddress(models.Model):
	user = models.ForeignKey(User, related_name="user_address", blank = False, \
						on_delete=models.CASCADE, null=True)
	town = models.ForeignKey(location_models.KenyaTown, blank = False, \
						on_delete=models.SET_NULL, null=True, related_name='user_town')
	estate_name = models.CharField(max_length = 25, blank = False, null= True)
	house_name = models.CharField(max_length = 25, blank = False, null= True)

	class Meta:
		verbose_name_plural = "User Address"
	
	def __str__(self):
		return f"{self.user.username} - {self.house_name},{self.estate_name},{self.town.town_name}."
	

class PhoneOTP(models.Model):
	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+254xxxxxxxxx'. Up to 14 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
	otp = models.CharField(max_length = 9, blank = True, null= True)
	count = models.IntegerField(default = 0, help_text = 'Number of times otp has been sent')
	logged = models.BooleanField(default = False, help_text = 'If otp verification got successful')
	# forgot = models.BooleanField(default = False, help_text = 'only true for forgot password')
	# forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


	def __str__(self):
		return str(self.phone) + ' is sent ' + str(self.otp)

	class Meta:
		verbose_name_plural = 'Phone Otp'

"""
# TODO:
Add password reset limit that restricts a user from resetting their password
more than x times in a day
"""
class ResetPasswordOTP(models.Model):
	email = models.EmailField(blank=True, null=True, unique=True)
	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+254xxxxxxxxx'. Up to 14 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
	otp = models.CharField(max_length = 9, blank = True, null= True)
	count = models.IntegerField(default = 0, help_text = 'Number of times otp has been sent')
	verified = models.BooleanField(default = False, help_text = 'If otp verification got successful')


	def __str__(self):
		rsp = ''
		if self.phone:
			rsp = 'OTP ' + str(self.otp) +  ' sent to ' + str(self.phone)
		elif self.email:
			rsp = 'OTP ' + str(self.otp) +  ' sent to ' + str(self.email)
		return rsp

	class Meta:
		verbose_name_plural = 'Reset Password OTP'

#Professional model tables from here
class ProfessionalGroup(models.Model):
	group_name = models.CharField(max_length=100, blank=False)
	group_image = CloudinaryField('image', blank=True, null=True, overwrite=True, resource_type='image',
							folder='professional_group_cover_photos')
	slug = models.SlugField(max_length=250, blank=True)
	interests = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, \
			related_name='group_interests')

	class Meta:
		verbose_name_plural = "ProfessionalGroups"

	def __str__(self):
		return self.group_name

class ProfessionalCategory(models.Model):
	professional_group = models.ForeignKey(ProfessionalGroup, on_delete=models.PROTECT,\
									default = None, related_name='pro_category_group')
	category_name = models.CharField(max_length=100, blank=False)
	category_image =  CloudinaryField('image', blank=True, null=True, overwrite=True, resource_type='image',
							folder='professional_group_cover_photos')
	slug = models.SlugField(max_length=250, blank=True)

	class Meta:
		verbose_name_plural = "ProfessionalCategories"

	def __str__(self):
		return self.category_name

class ProfessionalService(models.Model):
	professional_category = models.ForeignKey(ProfessionalCategory, on_delete=models.PROTECT,\
									default = None, related_name='pro_category', null =True)
	service_name = models.CharField(max_length=100, blank=False)
	service_image =  CloudinaryField('image', blank=True, null=True, overwrite=True, resource_type='image',
							folder='professional_group_cover_photos')
	slug = models.SlugField(max_length=250, blank=True)

	class Meta:
		verbose_name_plural = "ProfessionalServices"

	def __str__(self):
		return self.service_name

class ServiceSearchHistory(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, \
			null = True, related_name='user_service_search_history', on_delete=models.SET_NULL)
	professional_service = models.ForeignKey(ProfessionalService, on_delete=models.PROTECT,\
				default = None, related_name='pro_service_search_history', null =True, blank=True)
	project_location = models.ForeignKey(location_models.KenyaTown, blank = False, \
						on_delete=models.SET_NULL, null=True, related_name='project_location_service_search_history')
	search_count = models.PositiveIntegerField(default=0, null=True, blank=True)
	search_date = models.DateTimeField(auto_now = True, auto_now_add = False, null=True, blank=True)

	def __str__(self):
		return self.user.username if self.user else '' + ' ' + self.professional_service.service_name + ' ' + str(self.search_count)

	class Meta:
		verbose_name_plural = 'Service Search History'


class BusinessProfile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,\
			default = None, related_name='pro_business_profile')

	# the catgory the pro belongs to
	professional_category = models.ForeignKey(ProfessionalCategory, on_delete=models.SET_NULL,\
							default = None, related_name='pro_business_category', blank=False, null=True)
	professional_services = models.ManyToManyField(ProfessionalService, blank = True, \
							related_name='pro_business_services')

	# personal & contact information
	business_profile_image = CloudinaryField('image', blank=True, null=True, overwrite=True, resource_type='image',
								folder='business_page_profile_photos')
	business_name = models.CharField(max_length = 25, default=None, blank=True, null=True)
	phone = models.CharField(max_length=13, blank = True, null=True)
	business_email = models.EmailField(blank=True, null=True)
	address = models.CharField(max_length=250, blank=True, null=True)
	location = models.PointField(srid=4326, blank=True, null=True)
	website_link = models.URLField(max_length=200, blank=True, null=True)

	# social media accounts
	facebook_page_link = models.URLField(max_length=200, blank=True, null=True)
	twitter_page_link = models.URLField(max_length=200, blank=True, null=True)
	linkedin_page_link = models.URLField(max_length=200, blank=True, null=True)
	instagram_page_link = models.URLField(max_length=200, blank=True, null=True)

	# Professional information
	about_video = EmbedVideoField(blank = True, null = True)
	about = models.TextField(blank=True, null=True)
	# Additional area/s where this pro offers their professional services or areas where they would also want to find work
	service_areas = models.ManyToManyField(location_models.KenyaTown, blank = True, \
							related_name='service_areas')
	#network features
	saves = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, \
			related_name='business_page_saves')
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True,\
				related_name='business_page_followers')

	# admin reserved
	member_since = models.DateTimeField(auto_now=False, auto_now_add=True)
	featured = models.BooleanField(default=False, null=True, blank=True)
	verified = models.BooleanField(default=False)

	@property
	def percentage_complete(self):
		percent = {
		'business_profile_image': 10, 'professional_category':10, 'phone':5, 'business_email':10,
		'address':10, 'website_link':5, 'facebook_page_link': 5,
		'twitter_page_link': 5, 'linkedin_page_link':5, 'instagram_page_link':5,
		'location':10, 'about':20
		}
		total = 0
		if self.business_profile_image:
			total += percent.get('business_profile_image', 0)
		if self.professional_category:
			total += percent.get('professional_category', 0)
		if self.phone:
			total += percent.get('phone', 0)
		if self.address:
			total += percent.get('address', 0)
		if self.business_email:
			total += percent.get('business_email', 0)
		if self.website_link:
			total += percent.get('website_link', 0)
		if self.facebook_page_link:
			total += percent.get('facebook_page_link', 0)
		if self.twitter_page_link:
			total += percent.get('twitter_page_link', 0)
		if self.linkedin_page_link:
			total += percent.get('linkedin_page_link', 0)
		if self.instagram_page_link:
			total += percent.get('instagram_page_link', 0)
		if self.location:
			total += percent.get('location', 0)
		if self.about:
			total += percent.get('about', 0)
		return "%s"%(total)

	def get_absolute_url(self):
		return reverse( 'profiles:business_detail', kwargs={'pk':self.pk})

	def get_review_url(self):
		return reverse( 'profiles:business_review', kwargs={'pk':self.pk})

	class Meta:
		verbose_name_plural = 'BusinessProfile'

	def __str__(self):
		return self.business_name

	@property
	def longitude(self):
		return self.location.x

	@property
	def latitude(self):
		return self.location.y

	@property
	def average_rating(self):
		avg_rating = self.pro_business_review.all().aggregate(rating=Round(Avg('recommendation_rating')))
		return avg_rating['rating']

	@property
	def get_rating_stats(self):
		pro_reviews = self.pro_business_review.all()

		rvw_count = pro_reviews.count()
		if rvw_count == 0:
			rvw_count = 1

		recommendation_rating_avg = pro_reviews.aggregate(rating=Round(Avg('recommendation_rating')))['rating']
		responsive_rating_avg = pro_reviews.aggregate(rating=Round(Avg('responsive_rating')))['rating']
		knowledge_rating_avg = pro_reviews.aggregate(rating=Round(Avg('knowledge_rating')))['rating']
		professionalism_rating_avg = pro_reviews.aggregate(rating=Round(Avg('professionalism_rating')))['rating']
		quality_of_service_rating_avg = pro_reviews.aggregate(rating=Round(Avg('quality_of_service_rating')))['rating']

		five_star_ratings = pro_reviews.filter(recommendation_rating=5).count()
		four_star_ratings = pro_reviews.filter(recommendation_rating=4).count()
		three_star_ratings = pro_reviews.filter(recommendation_rating=3).count()
		two_star_ratings = pro_reviews.filter(recommendation_rating=2).count()
		one_star_ratings = pro_reviews.filter(recommendation_rating=1).count()

		array = {
		"five_stars": five_star_ratings/ rvw_count * 100,
		"four_stars": four_star_ratings / rvw_count * 100,
		"three_stars": three_star_ratings / rvw_count * 100,
		"two_stars": two_star_ratings / rvw_count * 100,
		"one_stars": one_star_ratings / rvw_count * 100,
		}

		highly_rated_traits = ['Responsiveness', 'Knowledge', 'Professionalism', 'Quality of service']
		if responsive_rating_avg and responsive_rating_avg >= 4.5:
			highly_rated_traits.append('Responsiveness')
		if knowledge_rating_avg and knowledge_rating_avg >= 4.5:
			highly_rated_traits.append('Knowledge')
		if professionalism_rating_avg and professionalism_rating_avg >= 4.5:
			highly_rated_traits.append('Professionalism')
		if quality_of_service_rating_avg and quality_of_service_rating_avg >= 4.5:
			highly_rated_traits.append('Quality of service')

		comment = ''

		if recommendation_rating_avg:
			if recommendation_rating_avg >= 4.5:
				comment = 'Very Highly rated'
			elif recommendation_rating_avg >= 3.5 and recommendation_rating_avg < 4.5:
				comment = 'Highly rated'
			elif recommendation_rating_avg >= 2.5 and recommendation_rating_avg < 3.5:
				comment = 'Rated Average'
			elif recommendation_rating_avg > 0 and recommendation_rating_avg < 1.5:
				comment = 'Rated Low'
			else:
				comment = 'Not Rated'
		else:
			comment = 'Not Rated'

		array = {
		"overall_rating": recommendation_rating_avg if recommendation_rating_avg else 0,
		"recommendation_rating_avg":recommendation_rating_avg if recommendation_rating_avg else 0,
		"responsive_rating_avg":responsive_rating_avg if recommendation_rating_avg else 0,
		"knowledge_rating_avg":knowledge_rating_avg if recommendation_rating_avg else 0,
		"professionalism_rating_avg":professionalism_rating_avg if recommendation_rating_avg else 0,
		"quality_of_service_rating_avg":quality_of_service_rating_avg if recommendation_rating_avg else 0,
		"highly_rated_traits":highly_rated_traits,
		"comment": comment,
		"stars_percentage_avg": array
		}

		return array

@receiver(pre_delete, sender=BusinessProfile)
def set_user_to_client(sender, instance, **kwargs):
	User.objects.filter(pk=instance.user.pk).update( user_type =  'CLIENT' )

class Client(models.Model):
	business_profile = models.ForeignKey(BusinessProfile, related_name = 'pro_business_client', on_delete = models.CASCADE)
	client_logo = CloudinaryField('image', blank=False, overwrite=True, resource_type='image',
							folder='client_logos')
	client_name = models.CharField(max_length = 25, blank=False)
	business_category = models.CharField(max_length = 25, blank=False)
	created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __str__(self):
		return  self.client_name + ' - ' + self.business_category

	class Meta:
		verbose_name_plural = "Clients"

class BusinessHours(models.Model):
	WEEKDAYS = [
	  (1, _("Monday")),
	  (2, _("Tuesday")),
	  (3, _("Wednesday")),
	  (4, _("Thursday")),
	  (5, _("Friday")),
	  (6, _("Saturday")),
	  (7, _("Sunday")),
	]
	business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='pro_business_hours', blank=True, null=True)
	weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)
	from_hour = models.TimeField(blank=True, null=True)
	to_hour = models.TimeField(blank=True, null=True)

	class Meta:
		ordering = ('weekday', 'from_hour')
		verbose_name_plural = 'BusinessHours'
		unique_together = ('weekday', 'from_hour', 'to_hour')

	def __unicode__(self):
		return u'%s: %s - %s' % (self.get_weekday_display(),
				self.from_hour, self.to_hour)

class Review(models.Model):
	recommendation_rating_choices = (
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
	professionalism_rating_choices = (
		(1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
		(4, 'Good'),(5, 'Very good'),
	)
	quality_rating_choices = (
		(1, 'Very poor'),(2, 'Poor'),(3, 'Average'),
		(4, 'Good'),(5, 'Very good'),
	)

	profile = models.ForeignKey(BusinessProfile, related_name='pro_business_review', on_delete=models.CASCADE)
	recommendation_rating = models.PositiveIntegerField(choices=recommendation_rating_choices, null=True)
	responsive_rating = models.PositiveIntegerField(choices=responsive_rating_choices, null=True)
	knowledge_rating = models.PositiveIntegerField(choices=knowledge_rating_choices, null=True)
	professionalism_rating = models.PositiveIntegerField(choices=professionalism_rating_choices, null=True)
	quality_of_service_rating = models.PositiveIntegerField(choices=quality_rating_choices, null=True)
	comment = models.TextField(null=True)
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_review', blank=True)
	reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pro_reviewer', on_delete=models.CASCADE, null=True)
	review_date = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return  'User ID: ' + str(self.profile.user.pk) + ' - ' + self.profile.user.email + ' - ' + 'Rated: '+ str(self.recommendation_rating)

	class Meta:
		verbose_name_plural = 'Reviews'

	@property
	def average_rating(self):
		return self.all().aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)

#Portfolio consists projects
class PortfolioItemBase(models.Model):
	name = models.CharField(max_length = 50, blank = False, null = True)
	description = models.TextField(blank = False, null = True)
	project_job_type = models.ForeignKey(ProfessionalService, on_delete=models.SET_NULL,\
				default = None, related_name='project_job_type', null =True, blank=False)
	project_location = models.ForeignKey(location_models.KenyaTown, blank = False, \
						on_delete=models.SET_NULL, null=True, related_name='project_location')
	project_cost = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank=False)
	project_duration = models.PositiveIntegerField(null=True, blank=False, help_text='Project duration_in days')
	project_year = models.PositiveIntegerField(null=True, blank=False,default=current_year(),
					validators=[MinValueValidator(1984), max_value_current_year])
	video = EmbedVideoField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now = False, auto_now_add = True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default = None, on_delete = models.CASCADE,
				 related_name='%(app_label)s_%(class)s_createdby_related',\
				 related_query_name="%(app_label)s_%(class)s_createdby")
				 #related_name=profiles_portfolioitem_createdby_related, related_query_name = profiles_portfolioitem_createdby


	class Meta:
		abstract = True

	def __str__(self):
		return str(self.created_by.username) + '-' + str(self.name)

class PortfolioItem(PortfolioItemBase):
	# we will reserve this for the future just incase conditions change
	# needing us to have unique fields and properties
	class Meta:
		verbose_name_plural = 'PortfolioItem'

class PortfolioItemPhoto(models.Model):
	portfolio_item = models.ForeignKey(PortfolioItem, related_name = "portfolio_item_photo", on_delete = models.CASCADE)
	photo = CloudinaryField('image', blank=True, overwrite=True, resource_type='image',
							folder='porfolio_item_photos')

	def save(self, *args, **kwargs):
		if not self.id:
			self.photo = self.compressImage(self.photo)
		super(PortfolioItemPhoto,   self).save(*args,   **kwargs)

	def compressImage(self,image):
		imageTemporary	=	Image.open(image)
		outputIoStream	=	BytesIO()
		imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=85) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage	=	InMemoryUploadedFile(outputIoStream,'CloudinaryField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

@receiver(pre_delete, sender=PortfolioItemPhoto)
def porfolio_item_photo_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.photo.public_id)

#professional teammates
class TeammateConnection(models.Model):
	accepted_choices = (
	('Yes', 'Yes'),
	('No' , 'No')
	)
	requestor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'connection_requestor', on_delete = models.CASCADE)
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'connection_request_receiver', on_delete = models.CASCADE)
	receiver_accepted = models.CharField(choices = accepted_choices, default = 'No', max_length = 3, blank = True, null=True)
	starred = models.BooleanField(default = False, blank=True, null=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return str(self.requestor) + " - " + str(self.receiver) + " - " + self.receiver_accepted

@receiver(post_save, sender=TeammateConnection)
def send_email_to_receiver(sender, instance, **kwargs):
	requestor_business_profile_pk = instance.requestor.pro_business_profile.pk
	receiver_business_profile_pk =  instance.receiver.pro_business_profile.pk
	# if the instance is that of accepting the connection request then send a
	# request accpted email message to the requestor
	if instance.receiver_accepted == 'Yes':
		profile_celery_tasks.send_connection_accepted_email.delay(requestor_business_profile_pk,receiver_business_profile_pk)
	# else this is a new connection request so send a request to connect email message
	else:
		profile_celery_tasks.send_connection_request_email.delay(requestor_business_profile_pk,receiver_business_profile_pk)

"""
Matchmaking model for holding Filter options that will allow for a better and
dynamic filtering process.
"""
class MatchMaker(models.Model):
	professional_service = models.OneToOneField(ProfessionalService, on_delete=models.CASCADE,\
							default = None, related_name='matchmaking_service')
	description = models.TextField()

	def __str__(self):
		return self.professional_service.service_name

	class Meta:
		verbose_name_plural = "Matchmaking Process"

class Question(models.Model):
	QUESTION_TYPE = (
	('MULTIPLE_CHOICE','Multiple Choice'),
	('SINGLE_CHOICE', 'Single Choice'),
	('TEXT_INPUT','Text Input')
	)
	step = models.PositiveIntegerField(default=0, help_text="The step where the question will appear")
	title = models.CharField(max_length=100, help_text="A short title of question e.g. Number of rooms, Cleaning Type")
	slug = models.SlugField(max_length=250, blank=True)
	client_question = models.TextField(help_text="The question that clients will be asked e.g. How many rooms are you painting?",null=True)
	pro_question= models.TextField(help_text="The question that professionals will be asked?", null=True)
	question_type = models.CharField(choices=QUESTION_TYPE, max_length=100, default='TEXT_INPUT', blank=False)
	matchMaker = models.ForeignKey(MatchMaker,on_delete=models.CASCADE,\
						default = None, related_name='matchmaker_question')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Matchmaking Questions"


class QuestionOptions(models.Model):
	question = models.ForeignKey(Question,on_delete=models.SET_NULL,\
							default = None, null=True, blank=False, related_name='question_option')
	name = models.CharField(max_length=100, null=True, blank=False, help_text="Option name")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Question Options"

class ClientAnswer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,\
			default = None, null=True, related_name='user_answer')
	question = models.ForeignKey(Question, on_delete=models.CASCADE,\
							default = None, related_name='question_answer')
	project_location = models.ForeignKey(location_models.KenyaTown, blank = False, \
						on_delete=models.SET_NULL, null=True, related_name='client_project_location')
	answer = models.ManyToManyField(QuestionOptions, blank=True, related_name='option_answer')
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.user.username + ' ' + self.question.title + ' ' + str(self.question.question_type)

class ProAnswer(models.Model):
	business_profile = models.ForeignKey(BusinessProfile, on_delete=models.SET_NULL,\
			default = None, null=True, related_name='match_answer')
	question = models.ForeignKey(Question, on_delete=models.CASCADE,\
							default = None, related_name='pro_question_answer')
	service_delivery_areas = models.ManyToManyField(location_models.KenyaTown, blank = False, \
								related_name='pro_service_delivery_areas')
	answer = models.ManyToManyField(QuestionOptions, blank=True, related_name='pro_option_answer')
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.business_profile.business_name + ' ' + str(self.question.question_type)
