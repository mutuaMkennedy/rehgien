from django import forms
from . import models
from django.forms import ClearableFileInput
from leaflet.forms.widgets import LeafletWidget
from cloudinary.forms import CloudinaryFileField
#from haystack.forms import FacetedSearchForm

class DateInput(forms.DateInput):
	input_type = 'date'

class TimeInput(forms.TimeInput):
	input_type = 'text'

class ListingForm(forms.ModelForm):
	appliances = forms.MultipleChoiceField(required=False, choices = models.Home.APPLIANCES_CHOICES, widget = forms.SelectMultiple())
	floor_covering = forms.MultipleChoiceField(required=False, choices = models.Home.FLOOR_COVERING_CHOICES, widget = forms.SelectMultiple())
	rooms = forms.MultipleChoiceField(required=False, choices = models.Home.ROOMS_CHOICES, widget = forms.SelectMultiple())
	indoor_features = forms.MultipleChoiceField(required=False, choices = models.Home.INDOOR_FEATURES_CHOICES, widget = forms.SelectMultiple())
	cooling_type = forms.MultipleChoiceField(required=False, choices = models.Home.COOLING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_type = forms.MultipleChoiceField(required=False, choices = models.Home.HEATING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_fuel = forms.MultipleChoiceField(required=False, choices = models.Home.HEATING_FUEL_CHOICES, widget = forms.SelectMultiple())
	building_amenities = forms.MultipleChoiceField(required=False, choices = models.Home.BUILDING_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	exterior = forms.MultipleChoiceField(required=False, choices = models.Home.EXTERIOR_CHOICES, widget = forms.SelectMultiple())
	outdoor_amenities = forms.MultipleChoiceField(required=False, choices = models.Home.OUTDOOR_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	parking = forms.MultipleChoiceField(required=False, choices = models.Home.PARKING_CHOICES, widget = forms.SelectMultiple())
	roof = forms.MultipleChoiceField(required=False, choices = models.Home.ROOF_CHOICES, widget = forms.SelectMultiple())
	view = forms.MultipleChoiceField(required=False, choices = models.Home.VIEW_CHOICES, widget = forms.SelectMultiple())
	basement = forms.ChoiceField(required = False, choices =models.Home.BASEMENT_CHOICES, widget=forms.RadioSelect())
	deal_closed = forms.ChoiceField(required = False, choices =models.Home.DEAL_CLOSED_CHOICES, widget=forms.RadioSelect())
	home_type = forms.ModelChoiceField(queryset=models.HomeType.objects, empty_label=None)
	class Meta:
		model = models.Home
		fields = [	'listing_type','property_name', 'price', 'home_type','virtual_tour_url','location_name', 'location', 'bathrooms', 'bedrooms', 'total_rooms',
					'floor_number','floor_area', 'number_of_units', 'number_of_stories',
					'parking_spaces', 'year_built', 'remodel_year','garage_sqm', 'appliances', 'basement', 'floor_covering',
					'rooms', 'indoor_features', 'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities', 'exterior',
					'outdoor_amenities', 'parking', 'roof', 'view', 'related_website', 'phone', 'email', 'description', 'deal_closed','final_closing_offer'
			]
		widgets = {'location':LeafletWidget()}

class AddressInfo(forms.ModelForm):
	lat = forms.FloatField(widget=forms.HiddenInput())
	long = forms.FloatField(widget=forms.HiddenInput())
	class Meta:
		model = models.Home
		fields = ['location_name']

class MapPoint(forms.ModelForm):
	class Meta:
		model = models.Home
		fields = ['location']
		widgets = {'location':LeafletWidget()}

class PropetyFacts(forms.ModelForm):
	appliances = forms.MultipleChoiceField(required=False, choices = models.Home.APPLIANCES_CHOICES, widget = forms.SelectMultiple())
	floor_covering = forms.MultipleChoiceField(required=False, choices = models.Home.FLOOR_COVERING_CHOICES, widget = forms.SelectMultiple())
	rooms = forms.MultipleChoiceField(required=False, choices = models.Home.ROOMS_CHOICES, widget = forms.SelectMultiple())
	indoor_features = forms.MultipleChoiceField(required=False, choices = models.Home.INDOOR_FEATURES_CHOICES, widget = forms.SelectMultiple())
	cooling_type = forms.MultipleChoiceField(required=False, choices = models.Home.COOLING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_type = forms.MultipleChoiceField(required=False, choices = models.Home.HEATING_TYPE_CHOICES, widget = forms.SelectMultiple())
	heating_fuel = forms.MultipleChoiceField(required=False, choices = models.Home.HEATING_FUEL_CHOICES, widget = forms.SelectMultiple())
	building_amenities = forms.MultipleChoiceField(required=False, choices = models.Home.BUILDING_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	exterior = forms.MultipleChoiceField(required=False, choices = models.Home.EXTERIOR_CHOICES, widget = forms.SelectMultiple())
	outdoor_amenities = forms.MultipleChoiceField(required=False, choices = models.Home.OUTDOOR_AMENITIES_CHOICES, widget = forms.SelectMultiple())
	parking = forms.MultipleChoiceField(required=False, choices = models.Home.PARKING_CHOICES, widget = forms.SelectMultiple())
	roof = forms.MultipleChoiceField(required=False, choices = models.Home.ROOF_CHOICES, widget = forms.SelectMultiple())
	view = forms.MultipleChoiceField(required=False, choices = models.Home.VIEW_CHOICES, widget = forms.SelectMultiple())
	basement = forms.ChoiceField(required = False, choices =models.Home.BASEMENT_CHOICES, widget=forms.RadioSelect())
	deal_closed = forms.ChoiceField(required = False, choices =models.Home.DEAL_CLOSED_CHOICES, widget=forms.RadioSelect())
	home_type = forms.ModelChoiceField(queryset=models.HomeType.objects, empty_label=None)
	class Meta:
		model = models.Home
		fields = [
		'listing_type','property_name', 'price', 'home_type','virtual_tour_url',
		'bathrooms', 'bedrooms', 'total_rooms', 'floor_number','floor_area',
		'number_of_units', 'number_of_stories', 'parking_spaces', 'year_built',
		'remodel_year','garage_sqm', 'appliances', 'basement', 'floor_covering',
		'rooms', 'indoor_features', 'cooling_type', 'heating_type', 'heating_fuel',
		'building_amenities', 'exterior','outdoor_amenities', 'parking', 'roof',
		'view', 'related_website', 'phone', 'email', 'description', 'deal_closed',
		'final_closing_offer'
		]

class PhotoForm(forms.ModelForm):
	photo = forms.ImageField(widget=forms.FileInput(attrs={'multiple':True}))
	class Meta:
		model = models.PropertyPhoto
		fields = ['photo',]
		photo = CloudinaryFileField(
				label = 'Property Photo',
				options = {
					'format':'jpg',
					'resource_type':'image',
				},
				)

class VideoForm(forms.ModelForm):
	video = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':False,'accept': 'video/*'}),required=False)
	class Meta:
		model = models.PropertyVideo
		fields = ['video',]
		# widgets = {
		# 	'video': ClearableFileInput(attrs={'multiple':False})
		# }

class OpenHouseForm(forms.ModelForm):
	class Meta:
		model = models.PropertyOpenHouse
		fields = ['date','start_time','end_time']
		widgets = {
			'date': DateInput(),'start_time':TimeInput(),'end_time':TimeInput()
		}
