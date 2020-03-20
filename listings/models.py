import sys
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from multiselectfield import MultiSelectField
from django.template.defaultfilters import slugify
from django.urls import reverse
from .validators import validate_video_extension
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.

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
	('SINGLEFAMILIY', 'Single family'), ('TERRACED', 'Terraced house'),
	('TOWNHOUSE', 'Townhouse'), ('OTHER', 'Other'),
	}
# User = settings.AUTH_USER_MODEL

class PropertyForSale(models.Model):
	#Property Facts
	property_name = models.CharField(max_length=20, default=None, db_index=True)
	type = models.CharField(max_length=20, choices = HOUSE_TYPE_CHOICES, default='APARTMENT')
	price = models.PositiveIntegerField(default=0)
	virtual_tour_url = models.CharField(max_length = 500, default = None)
	location_name = models.CharField(max_length= 20, default=None)
	location = models.PointField(srid=4326, default=None)
	thumb = models.ImageField(default=None, null=True)
	bathrooms = models.PositiveIntegerField(default=1, blank = True)
	bedrooms = models.PositiveIntegerField(default=1)
	total_rooms = models.PositiveIntegerField(default = 1, blank = False)
	floor_number = models.PositiveIntegerField(default = 0)
	description = models.TextField()
	floor_area = models.PositiveIntegerField(blank = True, default = 1.0)
	measurement_unit_choices = (
						('SQft', 'SqFt'),
						('SQm', 'SqM'),
								)
	size_units = models.CharField(max_length = 10,choices = measurement_unit_choices, default = 'SQFt')
	number_of_units = models.PositiveIntegerField(default = 1)
	number_of_stories = models.PositiveIntegerField(default = 0)
	parking_spaces = models.PositiveIntegerField(default = 1)
	year_built = models.PositiveIntegerField(blank = False, default = 2000)
	remodel_year = models.PositiveIntegerField(blank = True, null = True)
	garage_sqm = models.PositiveIntegerField(blank = True, default = 1)
	# open_house = models.DateField(auto_now = False, auto_now_add = False, editable = True, blank = True)
	#Additional Details(ROOM DETAILS)
	appliances = MultiSelectField(choices = APPLIANCES_CHOICES, default = None, blank = True)
	basement = models.CharField(max_length = 10, choices = BASEMENT_CHOICES, default = None, blank = True)
	floor_covering = MultiSelectField(choices = FLOOR_COVERING_CHOICES, default = None, blank = True)
	rooms = MultiSelectField(choices = ROOMS_CHOICES, default = None, blank = True)
	indoor_features = MultiSelectField(choices = INDOOR_FEATURES_CHOICES, default = None, blank = True)
	#Additional Details(UTILITY DETAILS)
	cooling_type = MultiSelectField(choices = COOLING_TYPE_CHOICES, default = None, blank = True)
	heating_type = MultiSelectField(choices = HEATING_TYPE_CHOICES, default = None, blank = True)
	heating_fuel = MultiSelectField(choices = HEATING_FUEL_CHOICES, default = None, blank = True)
	#Additional Details(BUILDING DETAILS)
	building_amenities = MultiSelectField(choices = BUILDING_AMENITIES_CHOICES, default = None, blank = True)
	exterior = MultiSelectField(choices = EXTERIOR_CHOICES, default = None, blank = True)
	outdoor_amenities = MultiSelectField(choices = OUTDOOR_AMENITIES_CHOICES, default = None, blank = True)
	parking = MultiSelectField(choices = PARKING_CHOICES, default = None, blank = True)
	roof = MultiSelectField(choices = ROOF_CHOICES, default = None, blank = True)
	view = MultiSelectField(choices = VIEW_CHOICES, default = None, blank = True)
	#owner Information
	related_website = models.CharField(max_length = 100, default = None)
	publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)
	owner = models.ForeignKey(User, default=None, related_name='sale_property', on_delete=models.CASCADE)
	phone = models.CharField(max_length=13)
	email = models.EmailField(blank=None)
	#likes = models.ManyToManyField(User, related_name = 'likes')
	#slug  = models.SlugField()

	#@property
	#def totallikes(self):
		#return self.likes.count()

	#def save(self, *args, **kwargs):
		#self.slug = slugify(self.name)
		#super(PropertyForSale, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		if not self.id:
			self.thumb = self.compressImage(self.thumb)
		super(PropertyForSale, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.thumb.delete()
    #     super().delete(*args, **kwargs)

	def compressImage(self,thumb):
		imageTemporary	=	Image.open(thumb)
		outputIoStream	=	BytesIO()
		imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=30) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage	=	InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % thumb.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	def get_absolute_url(self):
		return reverse( 'listings:onsale_detail', kwargs={'pk':self.pk} )

	def __str__(self):
		return self.property_name + '-' + '-' + self.phone + '-' + self.email

	class Meta:
		verbose_name_plural = 'PropertyForSale'

class PropertyForSaleImages(models.Model):
	property = models.ForeignKey(PropertyForSale, on_delete=models.CASCADE, related_name='images', null=True)
	image = models.ImageField(default=None, null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.image = self.compressImage(self.image)
		super(PropertyForSaleImages, self).save(*args, **kwargs)

	def compressImage(self,image):
		imageTemporary	=	Image.open(image)
		outputIoStream	=	BytesIO()
		imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=30) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage	=	InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	class Meta:
		verbose_name_plural = 'PropertyForSaleImages'

class PropertyForSaleVideos(models.Model):
	property = models.ForeignKey(PropertyForSale, on_delete=models.CASCADE, related_name= 'videos', null=True)
	video = models.FileField(upload_to='videos/', null=True, validators=[validate_video_extension])

	class Meta:
		verbose_name_plural = 'PropertyForSaleVideos'


class RentalProperty(models.Model):
	property_name = models.CharField(max_length = 20, blank = False)
	type = models.CharField(max_length = 20, choices = HOUSE_TYPE_CHOICES, default = 'APARTMENT')
	price = models.PositiveIntegerField(default=0)
	virtual_tour_url = models.CharField(max_length = 500, default = None)
	location_name = models.CharField(max_length= 100, default='Nairobi')
	location = models.PointField(srid=4326, default=None)
	thumb = models.ImageField(default=None)
	bathrooms = models.PositiveIntegerField(default=1, blank = True)
	bedrooms = models.PositiveIntegerField(default=1)
	total_rooms = models.PositiveIntegerField(default = 1, blank = False)
	floor_number = models.PositiveIntegerField(default = 0)
	description = models.TextField()
	floor_area= models.PositiveIntegerField(default = 1.0)
	measurement_unit_choices = (
						('SQft', 'SqFt'),
						('SQm', 'SqM'),
								)
	size_units = models.CharField(max_length = 10,choices = measurement_unit_choices, default = 'Acres')
	number_of_units = models.PositiveIntegerField(default = 1)
	number_of_stories = models.PositiveIntegerField(default = 0)
	parking_spaces = models.PositiveIntegerField(default = 1)
	year_built = models.PositiveIntegerField(blank = False, default = 2000)
	remodel_year = models.PositiveIntegerField(blank = True, null = True)
	# open_house = models.DateField(auto_now = False, auto_now_add = False, editable = True, blank = True)
	#Additional Details(ROOM DETAILS)
	appliances = MultiSelectField(choices = APPLIANCES_CHOICES, default = None, blank = True)
	basement = models.CharField(max_length = 10, choices = BASEMENT_CHOICES, default = None, blank = True)
	floor_covering = MultiSelectField(choices = FLOOR_COVERING_CHOICES, default = None, blank = True)
	rooms = MultiSelectField(choices = ROOMS_CHOICES, default = None, blank = True)
	indoor_features = MultiSelectField(choices = INDOOR_FEATURES_CHOICES, default = None, blank = True)
	#Additional Details(UTILITY DETAILS)
	cooling_type = MultiSelectField(choices = COOLING_TYPE_CHOICES, default = None, blank = True)
	heating_type = MultiSelectField(choices = HEATING_TYPE_CHOICES, default = None, blank = True)
	heating_fuel = MultiSelectField(choices = HEATING_FUEL_CHOICES, default = None, blank = True)
	#Additional Details(BUILDING DETAILS)
	building_amenities = MultiSelectField(choices = BUILDING_AMENITIES_CHOICES, default = None, blank = True)
	exterior = MultiSelectField(choices = EXTERIOR_CHOICES, default = None, blank = True)
	outdoor_amenities = MultiSelectField(choices = OUTDOOR_AMENITIES_CHOICES, default = None, blank = True)
	parking = MultiSelectField(choices = PARKING_CHOICES, default = None, blank = True)
	roof = MultiSelectField(choices = ROOF_CHOICES, default = None, blank = True)
	view = MultiSelectField(choices = VIEW_CHOICES, default = None, blank = True)
	#owner Information
	related_website = models.CharField(max_length = 100, default = None)
	publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)
	owner = models.ForeignKey(User, default=None, related_name='rent_property', on_delete=models.CASCADE)
	phone = models.CharField(max_length=13)
	email = models.EmailField(blank=None)

	def save(self, *args, **kwargs):
		if not self.id:
			self.thumb = self.compressImage(self.thumb)
		super(RentalProperty, self).save(*args, **kwargs)

	def compressImage(self,thumb):
		imageTemporary = Image.open(thumb)
		outputIoStream = BytesIO()
		imageTemporaryResized = imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=30) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % thumb.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	def get_absolute_url(self):
		return reverse( 'listings:rental_detail', kwargs={'pk':self.pk} )


	class Meta:
		verbose_name_plural = 'RentalProperty'

	def __str__(self):
		return self.property_name + '-' + '-' + self.type + '-' + self.phone + '-' + self.email


class RentalImages(models.Model):
	property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name='images', null=True)
	image = models.ImageField(default=None)

	def save(self, *args, **kwargs):
		if not self.id:
			self.image = self.compressImage(self.image)
		super(RentalImages, self).save(*args, **kwargs)

	def compressImage(self,image):
		imageTemporary	=	Image.open(image)
		outputIoStream	=	BytesIO()
		imageTemporaryResized	=	imageTemporary.resize( (1020,573) ) # Resize can be set to various varibale values in settings.py
		imageTemporary.save(outputIoStream , format='JPEG', quality=30) # change quality according to requirement.
		outputIoStream.seek(0)
		uploadedImage	=	InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	class Meta:
		verbose_name_plural = 'RentalImages'

class RentalVideos(models.Model):
	property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name= 'videos', null=True)
	video = models.FileField(upload_to='videos/', null=True)

	class Meta:
		verbose_name_plural = 'RentalVideos'
