import sys
from django.db import models
from django.conf import settings
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

class PropertyTypeImage(models.Model):
	apartment = models.ImageField(upload_to='categoryImages/', null=True, blank=True)
	bungalow = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	condominium = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	dormitory = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	duplex = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	mansion = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	single_family = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	terraced_house = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	townhouse = models.ImageField(upload_to='categoryImages/',null=True, blank=True)
	other = models.ImageField(upload_to='categoryImages/',null=True, blank=True)

	def save(self,*args,**kwargs):
		if not self.pk and PropertyTypeImage.objects.exists():
			raise	ValidationError('There can be only one PropertyTypeImage instance')
			return	super(PropertyTypeImage,	self).save(*args,	**kwargs)

	class Meta:
		verbose_name_plural = 'PropertyTypeImages'

class PropertyBase(models.Model):
	property_name = models.CharField(max_length=20, default=None, db_index=True)
	price = models.PositiveIntegerField(default=0)
	virtual_tour_url = models.CharField(max_length = 500, default = None)
	location_name = models.CharField(max_length= 20, default=None)
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

	phone = models.CharField(max_length=13)
	email = models.EmailField(blank=None)
	publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.property_name + '-' + '-' + self.phone + '-' + self.email

	@property
	def longitude(self):
		return self.location.x

	@property
	def latitude(self):
		return self.location.y

	@property
	def totalsaves(self):
		return self.saves.count()

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
	('for_sale','for_sale'),
	('for_rent','for_rent')
	)
	PROPERTY_CATEGORY_CHOICES = (
		('homes','homes'),
	)
	#Property Facts
	listing_type = models.CharField(max_length=20, choices = LISTING_TYPE_CHOICES, default='for_sale')
	property_category = models.CharField(max_length=20, choices = PROPERTY_CATEGORY_CHOICES, default='homes')
	type = models.CharField(max_length=20, choices = HOUSE_TYPE_CHOICES, default='APARTMENT')
	bathrooms = models.PositiveIntegerField(default=1, blank = True)
	bedrooms = models.PositiveIntegerField(default=1)
	total_rooms = models.PositiveIntegerField(default = 1, blank = False)
	floor_number = models.PositiveIntegerField(default = 0)
	number_of_stories = models.PositiveIntegerField(default = 0)
	parking_spaces = models.PositiveIntegerField(default = 1)
	year_built = models.PositiveIntegerField(blank = False, default = 2000)
	remodel_year = models.PositiveIntegerField(blank = True, null = True)
	garage_sqm = models.PositiveIntegerField(blank = True, default = 1)
	#Additional Details#
	#ROOM DETAILS
	appliances = MultiSelectField(choices = APPLIANCES_CHOICES, default = None, blank = True)
	basement = models.CharField(max_length = 10, choices = BASEMENT_CHOICES, default = None, blank = True)
	floor_covering = MultiSelectField(choices = FLOOR_COVERING_CHOICES, default = None, blank = True)
	rooms = MultiSelectField(choices = ROOMS_CHOICES, default = None, blank = True)
	indoor_features = MultiSelectField(choices = INDOOR_FEATURES_CHOICES, default = None, blank = True)
	#UTILITY DETAILS
	cooling_type = MultiSelectField(choices = COOLING_TYPE_CHOICES, default = None, blank = True)
	heating_type = MultiSelectField(choices = HEATING_TYPE_CHOICES, default = None, blank = True)
	heating_fuel = MultiSelectField(choices = HEATING_FUEL_CHOICES, default = None, blank = True)
	#BUILDING DETAILS
	building_amenities = MultiSelectField(choices = BUILDING_AMENITIES_CHOICES, default = None, blank = True)
	exterior = MultiSelectField(choices = EXTERIOR_CHOICES, default = None, blank = True)
	outdoor_amenities = MultiSelectField(choices = OUTDOOR_AMENITIES_CHOICES, default = None, blank = True)
	parking = MultiSelectField(choices = PARKING_CHOICES, default = None, blank = True)
	roof = MultiSelectField(choices = ROOF_CHOICES, default = None, blank = True)
	view = MultiSelectField(choices = VIEW_CHOICES, default = None, blank = True)


	def get_absolute_url(self):
		return reverse( 'listings:property_detail', kwargs={'pk':self.pk, 'property_category':self.property_category} )


	class Meta:
		verbose_name_plural = 'Homes'


class PropertyPhoto(models.Model):
	home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='home_photos', null=True)
	photo = CloudinaryField('photo', blank=True, overwrite=True, resource_type='image',
	 						folder='property_photos')

	def save(self, *args, **kwargs):
		if not self.id:
			self.photo = self.compressImage(self.photo)
		super(PropertyPhoto, self).save(*args, **kwargs)

	def compressImage(self,image):
		imageTemporary	=	Image.open(image)
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
	video = CloudinaryField('video', resource_type='video', folder='Property_Video', null=True, validators=[validate_video_extension])

	class Meta:
		verbose_name_plural = 'PropertyVideo'

@receiver(pre_delete, sender=PropertyVideo)
def video_delete(sender, instance, **kwargs):
	cloudinary.uploader.destroy(instance.video.public_id)
