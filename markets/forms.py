from django import forms
from django.forms.widgets import SelectDateWidget
from leaflet.forms.widgets import LeafletWidget
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class RequestPropertyForm(forms.ModelForm):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )
    general_features = forms.MultipleChoiceField(required=False, choices =GENERAL_FEATURES, widget = forms.SelectMultiple())
    parking_choices = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
    class Meta:
        model = models.PropertyRequestLead
        fields = [
        'property_type', "max_price", "min_price", "max_beds", "min_beds",
        "property_size", "location","general_features","parking_choices",
        "additional_details", "ownership",'number_of_units',
        "timeline", "name", "phone", "email","profile_image"
        ]
        widgets = {
            'timeline': DateInput(),
        }

class RequestProffesionalForm(forms.ModelForm):
    class Meta:
        model = models.ProffesionalRequestLead
        fields = [
        "type_of_proffesional", "location", "service_details","timeline", "name",
        "phone", "email","profile_image"
        ]
        widgets = {
            'timeline': DateInput(),
        }

class OtherRequestForm(forms.ModelForm):
    class Meta:
        model = models.OtherServiceLead
        fields = [
        "location", "service_details", "timeline", "name", "phone", "email","profile_image"
        ]
        widgets = {
            'timeline': DateInput(),
        }

class AgentLeadRequestForm(forms.ModelForm):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )
    general_features = forms.MultipleChoiceField(required=False, choices =GENERAL_FEATURES, widget = forms.SelectMultiple())
    parking_choices = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
    class Meta:
        model = models.AgentLeadRequest
        fields = ["property_type", "price", "price_negotiable", "beds", "property_size",
        "location_name", "location", "general_features", "parking_choices", "additional_details",
        "market_value", "number_of_units", "ownership", "timeline", "name", "phone", "email","profile_image"
        ]
        widgets = {
            'timeline': DateInput(),
            'location':LeafletWidget()
        }

class AgentPropertyRequestForm(forms.ModelForm):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )
    general_features = forms.MultipleChoiceField(required=False, choices =GENERAL_FEATURES, widget = forms.SelectMultiple())
    parking_choices = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
    class Meta:
        model = models.AgentPropertyRequest
        fields = ["property_type", "max_price", "min_price", "max_beds", "min_beds",
        "property_size", "location_name", "general_features", "parking_choices",
        "additional_details", "market_value", "number_of_units", "ownership",
        "timeline", "name", "phone", "email","profile_image"
        ]
        widgets = {
            'timeline': DateInput(),
        }
