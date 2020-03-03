from django import forms
from . import models
from django.forms import ClearableFileInput
from leaflet.forms.widgets import LeafletWidget
#from haystack.forms import FacetedSearchForm


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
			('WALL', 'Wall'), ('OTH', 'Other'),('NON', 'None')
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

class ListingForm(forms.ModelForm):
	appliances = forms.MultipleChoiceField(required=False, choices =APPLIANCES_CHOICES, widget = forms.SelectMultiple())
	floor_covering = forms.MultipleChoiceField(required=False, choices =FLOOR_COVERING_CHOICES, widget = forms.SelectMultiple())
	rooms = forms.MultipleChoiceField(required=False, choices =ROOMS_CHOICES, widget = forms.SelectMultiple())
	indoor_features = forms.MultipleChoiceField(required=False, choices =INDOOR_FEATURES_CHOICES, widget = forms.SelectMultiple())
	cooling_type = forms.MultipleChoiceField(required=False, choices =COOLING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_type = forms.MultipleChoiceField(required=False, choices =HEATING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_fuel = forms.MultipleChoiceField(required=False, choices =HEATING_FUEL_CHOICES, widget = forms.SelectMultiple())
	building_amenities = forms.MultipleChoiceField(required=False, choices =BUILDING_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	exterior = forms.MultipleChoiceField(required=False, choices =EXTERIOR_CHOICES, widget = forms.SelectMultiple())
	outdoor_amenities = forms.MultipleChoiceField(required=False, choices =OUTDOOR_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	parking = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
	roof = forms.MultipleChoiceField(required=False, choices =ROOF_CHOICES, widget = forms.SelectMultiple())
	view = forms.MultipleChoiceField(required=False, choices =VIEW_CHOICES, widget = forms.SelectMultiple())
	class Meta:
		model = models.PropertyForSale
		fields = ['property_name', 'price', 'type','virtual_tour_url','location_name', 'location', 'bathrooms', 'bedrooms', 'total_rooms',
					'floor_number','floor_area', 'size_units', 'number_of_units', 'number_of_stories',
					'parking_spaces', 'year_built', 'remodel_year','garage_sqm', 'appliances', 'basement', 'floor_covering',
					'rooms', 'indoor_features', 'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities', 'exterior',
					'outdoor_amenities', 'parking', 'roof', 'view', 'related_website', 'phone', 'email', 'thumb', 'description',
			]
		widgets = {'location':LeafletWidget()}

class ImageForm(forms.ModelForm):
	class Meta:
		model = models.PropertyForSaleImages
		fields = ['image',]
		widgets = {
			'image': ClearableFileInput(attrs={'multiple':True})
		}

class VideoForm(forms.ModelForm):
	class Meta:
		model = models.PropertyForSaleVideos
		fields = ['video',]
		widgets = {
			'video': ClearableFileInput(attrs={'multiple':False})
		}

class RentalListingForm(forms.ModelForm):
	appliances = forms.MultipleChoiceField(required=False, choices =APPLIANCES_CHOICES, widget = forms.SelectMultiple())
	floor_covering = forms.MultipleChoiceField(required=False, choices =FLOOR_COVERING_CHOICES, widget = forms.SelectMultiple())
	rooms = forms.MultipleChoiceField(required=False, choices =ROOMS_CHOICES, widget = forms.SelectMultiple())
	indoor_features = forms.MultipleChoiceField(required=False, choices =INDOOR_FEATURES_CHOICES, widget = forms.SelectMultiple())
	cooling_type = forms.MultipleChoiceField(required=False, choices =COOLING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_type = forms.MultipleChoiceField(required=False, choices =HEATING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_fuel = forms.MultipleChoiceField(required=False, choices =HEATING_FUEL_CHOICES, widget = forms.SelectMultiple())
	building_amenities = forms.MultipleChoiceField(required=False, choices =BUILDING_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	exterior = forms.MultipleChoiceField(required=False, choices =EXTERIOR_CHOICES, widget = forms.SelectMultiple())
	outdoor_amenities = forms.MultipleChoiceField(required=False, choices =OUTDOOR_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	parking = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
	roof = forms.MultipleChoiceField(required=False, choices =ROOF_CHOICES, widget = forms.SelectMultiple())
	view = forms.MultipleChoiceField(required=False, choices =VIEW_CHOICES, widget = forms.SelectMultiple())
	class Meta:
		model = models.RentalProperty
		fields = ['property_name', 'type', 'price', 'virtual_tour_url','location_name', 'location', 'bathrooms', 'bedrooms', 'total_rooms',
					'floor_number','floor_area', 'size_units', 'number_of_units', 'number_of_stories',
					'parking_spaces', 'year_built', 'remodel_year', 'appliances', 'basement', 'floor_covering',
					'rooms', 'indoor_features', 'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities', 'exterior',
					'outdoor_amenities', 'parking', 'roof', 'view', 'related_website', 'phone', 'email', 'thumb',
			]
		widgets = {'location':LeafletWidget()}

class RentalImageForm(forms.ModelForm):
	class Meta:
		model = models.RentalImages
		fields = ['image',]
		widgets = {
			'image': ClearableFileInput(attrs={'multiple':True})
		}

class RentalVideoForm(forms.ModelForm):
	class Meta:
		model = models.RentalVideos
		fields = ['video',]
		widgets = {
			'video': ClearableFileInput(attrs={'multiple':False})
		}
#for haystack
"""
class FacetedSaleSearchForm(FacetedSearchForm):

	def __init__(self, *args, **kwargs):
		data = dict(kwargs.get("data", []))
		self.location_names = data.get('location_name', [])
		self.types = data.get('type', [])
		self.bathrooms = data.get('bathrooms', [])
		self.bedrooms = data.get('bedrooms', [])
		super(FacetedSaleSearchForm, self).__init__(*args, **kwargs)

	def search(self):
		sqs = super(FacetedSaleSearchForm, self).search()
		if self.location_names:
			query = None
			for category in self.location_names:
				if query:
					query += u' OR '
				else:
					query = u''
				query += u'"%s"' % sqs.query.clean(location_name)
			sqs = sqs.narrow(u'location_name_exact:%s' % query)
		if self.types:
			query = None
			for brand in self.types:
				if query:
					query += u' OR '
				else:
					query = u''
				query += u'"%s"' % sqs.query.clean(type)
			sqs = sqs.narrow(u'types_exact:%s' % query)
		if self.bathrooms:
			query = None
			for brand in self.bathrooms:
				if query:
					query += u' OR '
				else:
					query = u''
				query += u'"%s"' % sqs.query.clean(bathrooms)
			sqs = sqs.narrow(u'bathrooms_exact:%s' % query)
		if self.bedrooms:
			query = None
			for brand in self.bedrooms:
				if query:
					query += u' OR '
				else:
					query = u''
				query += u'"%s"' % sqs.query.clean(bedrooms)
			sqs = sqs.narrow(u'bedrooms_exact:%s' % query)
		return sqs
"""
