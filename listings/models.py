import sys
from django.db import models
from django.db.models import Avg, Sum
import datetime
from django.conf import settings
from django.utils import timezone
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from multiselectfield import MultiSelectField
from django.template.defaultfilters import slugify
from django.urls import reverse
from .validators import validate_video_extension
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import cloudinary
from .regression import trendline as trend


#This model will allow easy addition of other property type requiring this fields
class PropertyType(models.Model):
	name = models.CharField(max_length = 50, blank=True, null = True)
	photo = models.ImageField(upload_to='propertyTypePhotos/', null=True, blank=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.name

class HomeType(PropertyType):
	# We will reserve this for any future modifications
	class Meta:
		verbose_name_plural = 'HomeTypes'

class PropertyBase(models.Model):
	property_name = models.CharField(max_length=120, default=None, db_index=True)
	price = models.PositiveIntegerField(default=0)
	virtual_tour_url = models.URLField(default = None, null=True, blank=True)
	location_name = models.CharField(max_length= 120, default=None)
	location = models.PointField(srid=4326, default=None)
	description = models.TextField()
	floor_area = models.PositiveIntegerField(blank = True, default = 1.0)
	number_of_units = models.PositiveIntegerField(default = 1)
	saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= \
		'%(app_label)s_%(class)s_saves_related', related_query_name="%(app_label)s_%(class)s_saves", \
		 blank =True) #related_name=listings_home_saves_related, related_query_name = listings_home_saves
	#Owners info
	related_website = models.CharField(max_length = 100, default = None)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, \
		related_name='%(app_label)s_%(class)s_owner_related', \
		related_query_name="%(app_label)s_%(class)s_owner", \
		on_delete=models.CASCADE)#related_name=listings_home_owner_related, related_query_name = listings_home_owner
	featured = models.BooleanField(default=False, null=True, blank=True)
	phone = models.CharField(max_length=13)
	email = models.EmailField(blank=None)
	publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)
	# This will be turn to False after 30 days from the publishdate
	is_active = models.BooleanField(default=True)
	# only displayed in the update form
	DEAL_CLOSED_CHOICES = (
		('YES', 'yes'),
		('NO', 'No'),
	)
	deal_closed = models.CharField( choices=DEAL_CLOSED_CHOICES, max_length = 3, default='NO')
	final_closing_offer = models.PositiveIntegerField(default=None, blank=True, null=True)

	class Meta:
		abstract = True
	#
	# def __str__(self):
	# 	return self.property_name + '-' + self.phone + '-' + self.email

	@property
	def longitude(self):
		return self.location.x

	@property
	def latitude(self):
		return self.location.y

	@property
	def totalsaves(self):
		return self.saves.count()

	@property
	def active_until(self):
		return self.publishdate + datetime.timedelta(days = 30 )

class Home(PropertyBase):
	# Lists for multiple choice fields
	APPLIANCES_CHOICES = (
				('DISH', 'Dishwasher'), ('GARB', 'Garbage disposal'),
	 			('OVEN', 'Oven'), ('REFRIG', 'Refrigerator'),
				('NON', 'None')
	)

	BASEMENT_CHOICES = (
			('FINI', 'Finished'), ('UNFI', 'Unfinished'),
	 		('PART', 'Partially finished'), ('NON', 'None'),
	)

	FLOOR_COVERING_CHOICES  = (
				('CARP', 'Carpet'), ('CONC', 'Concrete'), ('HARD', 'Hardwood'),
				('TILE', 'Tile'), ('SOFT', 'SoftWood'), ('OTH', 'Other'),
	)

	ROOMS_CHOICES = (
			('BREA', 'BreakFast nook'), ('DINI', 'Dining room'), ('FAMI', 'Family room'),
			('LIBR', 'Library'), ('MAST', 'Master bath'), ('MUDR', 'Mud room'),
			('OF', 'Office'), ('PANT', 'Pantry'), ('RECR', 'Recreation room'),
			('WORK', 'Workshop'), ('So/AR', 'Solarium/Atrium'), ('SUNR', 'Sun room'),
			('WALK', 'walk-in-closet'),
	)

	INDOOR_FEATURES_CHOICES = (
					('ATTI', 'Attic'), ('CEIL', 'Ceiling fans'),
					('DOUB', 'Double pane windows'), ('FIRE', 'Fireplace'),
					('SECU', 'Security system'), ('SKYL', 'Skylights'),
					('VAUL', 'Vaulted ceiling'),
	)

	COOLING_TYPE_CHOICES = (
				('CENT', 'Central'), ('EVAP', 'Evaporative'),
				('GEOT', 'Geothermal'), ('REFR', 'Refrigeration'),
				('SOLA', 'Solar'), ('WALL', 'Wall'),
				('OTHE', 'Other'), ('NON', 'None'),
	)

	HEATING_TYPE_CHOICES = (
				('BASE', 'Baseboard'), ('FORC', 'Forced air'),
				('GEOT', 'Geothermal'), ('HEAT', 'Heat pump'),
				('RADI', 'Radiant'), ('STOV', 'Stove'),
				('WALL', 'Wall'), ('OTH', 'Other'),
	)

	HEATING_FUEL_CHOICES = (
				('COAL', 'Coal'), ('ELEC', 'Electric'),
				('GAS', 'Gas'), ('OIL', 'Oil'),
				('PR/BU', 'Propane/Butane'), ('SOLA', 'Solar'),
				('WO/PE', 'Wood/Pelet'), ('OTH', 'Other'),
				('NON', 'None'),
	)

	BUILDING_AMENITIES_CHOICES = (
					('BASK', 'Basketball court'), ('CONT', 'Controlled access'),
					('DISA', 'Disabled access'), ('DOOR', 'Doorman'),
					('ELEV', 'Elevator'), ('FITN', 'Fitness Center'),
					('GATE', 'Gated entry'), ('NEAR', 'Near Transportation'),
					('SPOR', 'Sports court'),
	)

	EXTERIOR_CHOICES = (
			('BRIC', 'Brick'), ('CE/CO', 'Cement/Concrete'),
			('STON', 'Stone'), ('VINY', 'Vinyl'),
			('WOOD', 'Wood'), ('OTH', 'Other'),
	)

	OUTDOOR_AMENITIES_CHOICES = (
				('BALC', 'Balcony'), ('FENC', 'Fenced yard'),
				('GARD', 'Garden'), ('GREEN', 'Greenhouse'),
				('LAWN', 'Lawn'), ('POND', 'Pond'),
				('POOL', 'Pool'), ('SAUN', 'Sauna'),
				('SPRI', 'Sprinkler system'), ('wATER', 'Waterfront'),
	)

	PARKING_CHOICES = (
				('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
				('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
				('ONST', 'On-street'), ('NON', 'None'),
	)

	ROOF_CHOICES = (
			('ASPH', 'Asphalt'), ('TILE', 'Tile'),
			('SLAT', 'Slate'), ('OTH', 'Other'),
	)

	VIEW_CHOICES = (
			('CITY', 'City'), ('TERR', 'Territorial'),
			('MOUN', 'Mountain'), ('WATE', 'Water'),
			('PARK', 'Park'), ('NON', 'None'),
	)
	# HOUSE TYPES choices
	HOUSE_TYPE_CHOICES = {
		('APARTMENT', 'Apartment'), ('BUNGALOW', 'Bungalow'),
		('CONDOMINIUM', 'Condominium'), ('DORMITORY', 'Dormitory'),
		('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'),
		('SINGLEFAMILY', 'Single family'), ('TERRACED', 'Terraced house'),
		('TOWNHOUSE', 'Townhouse'), ('OTHER', 'Other'),
		}

	LISTING_TYPE_CHOICES = (
	('FOR_SALE','for sale'),
	('FOR_RENT','for rent')
	)
	PROPERTY_CATEGORY_CHOICES = (
		('HOMES','homes'),
	)
	#Property Facts
	listing_type = models.CharField(max_length=20, choices = LISTING_TYPE_CHOICES, default='FOR_SALE')
	property_category = models.CharField(max_length=20, choices = PROPERTY_CATEGORY_CHOICES, default='HOMES')
	home_type = models.ForeignKey(HomeType, on_delete=models.SET_NULL,\
	                                    default = None, related_name='home_type', null=True)
	bathrooms = models.PositiveIntegerField(default=1, blank = True)
	bedrooms = models.PositiveIntegerField(default=1)
	total_rooms = models.PositiveIntegerField(default = 1, blank = False)
	floor_number = models.PositiveIntegerField(default = 0,blank = True, null=True)
	number_of_stories = models.PositiveIntegerField(default = 0, blank = True, null=True)
	parking_spaces = models.PositiveIntegerField(default = 1,null=True, blank = True)
	year_built = models.PositiveIntegerField(blank = False, default = 2000, null=True)
	remodel_year = models.PositiveIntegerField(blank = True, null = True)
	garage_sqm = models.PositiveIntegerField(blank = True, default = 1,null=True)
	#Additional Details#
	#ROOM DETAILS
	appliances = MultiSelectField(choices = APPLIANCES_CHOICES, default = None, blank = True, null=True)
	basement = models.CharField(max_length = 10, choices = BASEMENT_CHOICES, default = None, blank = True,null=True)
	floor_covering = MultiSelectField(choices = FLOOR_COVERING_CHOICES, default = None, blank = True,null=True)
	rooms = MultiSelectField(choices = ROOMS_CHOICES, default = None, blank = True,null=True)
	indoor_features = MultiSelectField(choices = INDOOR_FEATURES_CHOICES, default = None, blank = True,null=True)
	#UTILITY DETAILS
	cooling_type = MultiSelectField(choices = COOLING_TYPE_CHOICES, default = None, blank = True, null=True)
	heating_type = MultiSelectField(choices = HEATING_TYPE_CHOICES, default = None, blank = True, null=True)
	heating_fuel = MultiSelectField(choices = HEATING_FUEL_CHOICES, default = None, blank = True, null=True)
	#BUILDING DETAILS
	building_amenities = MultiSelectField(choices = BUILDING_AMENITIES_CHOICES, default = None, blank = True, null=True)
	exterior = MultiSelectField(choices = EXTERIOR_CHOICES, default = None, blank = True, null=True)
	outdoor_amenities = MultiSelectField(choices = OUTDOOR_AMENITIES_CHOICES, default = None, blank = True, null=True)
	parking = MultiSelectField(choices = PARKING_CHOICES, default = None, blank = True, null=True)
	roof = MultiSelectField(choices = ROOF_CHOICES, default = None, blank = True, null=True)
	view = MultiSelectField(choices = VIEW_CHOICES, default = None, blank = True, null=True)

	class Meta:
		verbose_name_plural = 'Homes'

	def get_absolute_url(self):
		return reverse( 'listings:property_detail', kwargs={'pk':self.pk, 'property_category':self.property_category.lower()} )

	@property
	def similar_homes_this_area(self):
		homes = Home.objects.filter(	\
								price__range = (self.price - self.price * 0.2, self.price + self.price * 0.2),
								location_name__icontains = self.location_name.split(',')[-1]
								).exclude(id = self.id)[:10]
		return homes
	@property
	def similar_homes_this_region(self):
		home = Home.objects.filter(	\
						price__range = (self.price - self.price * 0.2, self.price + self.price * 0.2),
						location_name__icontains = self.location_name.split(',')[0]
						).exclude(id = self.id)[:10]
		return home

	@property
	def total_views_count(self):
		count = self.home_interactions.all().aggregate(Sum('views_count')).get('views_count__sum', 0)
		if count == None:
			return 0
		else:
			return count

	@property
	def recent_views_count(self):
		count = self.home_interactions.filter(created_at__gte =  timezone.now() - datetime.timedelta(hours = 24) )\
				.aggregate(Sum('views_count')).get('views_count__sum', 0)
		if count == None:
			return 0
		else:
			return count

	@property
	def views_trend(self):
		tt_views_array = []
		for n_days in range(0,25): # in the last 24 hours
			total_views = self.home_interactions.filter(created_at__gte = timezone.now() - datetime.timedelta(hours = n_days) )\
							.aggregate(Sum('views_count')).get('views_count__sum', 0)
			if total_views == None:
				total_views = 0
			tt_views_array.append(total_views)
		views_index = list(range(1,len(tt_views_array)+1 ) )
		trend_line = trend(views_index,tt_views_array)
		return trend_line

	@property
	def all_leads(self):
		return self.home_interactions.filter(is_lead=True)

class PropertyPhoto(models.Model):
	home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='home_photos', null=True)
	photo = CloudinaryField('photo', blank=True, overwrite=True, resource_type='image',
	 						folder='property_photos')

	__initial_photo = None

	def __init__(self, *args, **kwargs):
		super(PropertyPhoto, self).__init__(*args, **kwargs)
		self.__initial_photo = self.photo

	def save(self, *args, **kwargs):
		# We check if the photo object exists, if not we compress the new photo uploaded
		# this will fire mostly on innitial saves
		if not self.id:
			self.photo = self.compressImage(self.photo)
		# When the photo field is updated the photo will not be compressed,
		# so we match the original photo value
		# and the new one and if it has changed we compress the photo
		elif self.photo != self.__initial_photo:
			self.photo = self.compressImage(self.photo)
		super(PropertyPhoto, self).save(*args, **kwargs)

	def compressImage(self,image):
		imageTemporary	=	Image.open(image).convert('RGB')
		outputIoStream	=	BytesIO()
		imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=70) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage	=	InMemoryUploadedFile(outputIoStream,'CloudinaryField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	class Meta:
		verbose_name_plural = 'PropertyPhoto'

@receiver(pre_delete, sender=PropertyPhoto)
def photo_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.photo.public_id)


class PropertyVideo(models.Model):
	home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name= 'home_video', null=True)
	video = CloudinaryField('video', resource_type='video', folder='Property_Video', null=True, validators=[validate_video_extension], blank=True)

	class Meta:
		verbose_name_plural = 'PropertyVideo'

@receiver(pre_delete, sender=PropertyVideo)
def video_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.video.public_id)

class PropertyOpenHouse(models.Model):
	home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name= 'home_openhouse', null=True)
	date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,default=None)
	start_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None)
	end_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None)
	reminder_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'open_house_reminder_list', blank=True, default=None)

	class Meta:
		verbose_name_plural = 'PropertyOpenHouses'

class PropertyInteraction(models.Model):
	home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name= 'home_interactions', null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user_property_interation", null=True, default=None)
	is_lead = models.BooleanField(default=False, null=True, blank=True)
	has_viewed = models.BooleanField(default=False, null=True, blank=True)
	views_count = models.PositiveIntegerField(default=None, null=True,blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)


	class Meta:
		verbose_name_plural = 'PropertyInteractions'

	def __str__(self):
		return str(self.user.username) + ' ' +  str(self.is_lead) + ' ' + str(self.has_viewed)

class SavedSearch(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name= 'user_saved_search')
	search_url = models.TextField(blank=False,default=None, null=True)
