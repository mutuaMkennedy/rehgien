from django import forms
from django.forms.widgets import SelectDateWidget
from . import models

GENERAL_FEATURES = (
    ('FURNISHED', 'Furnished'),
    ('SERVICED', 'Serviced')
)
PARKING_CHOICES = (
			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
			('ONST', 'On-street'), ('NON', 'None'),
)

class DateInput(forms.DateInput):
    input_type = 'date'

class RequestPropertyForm(forms.ModelForm):
    general_features = forms.MultipleChoiceField(required=False, choices =GENERAL_FEATURES, widget = forms.SelectMultiple())
    parking_choices = forms.MultipleChoiceField(required=False, choices =PARKING_CHOICES, widget = forms.SelectMultiple())
    class Meta:
        model = models.PropertyRequestLead
        fields = [
        'property_type', "max_price", "min_price", "max_beds", "min_beds",
        "property_size", "location","general_features","parking_choices",
        "additional_details", "ownership",
        "timeline", "name", "phone", "email"
        ]
        widgets = {
            'timeline': DateInput(),
        }

class RequestProffesionalForm(forms.ModelForm):
    class Meta:
        model = models.ProffesionalRequestLead
        fields = [
        "type_of_proffesional", "location", "service_details","timeline", "name",
        "phone", "email"
        ]
        widgets = {
            'timeline': DateInput(),
        }

class OtherRequestForm(forms.ModelForm):
    class Meta:
        model = models.OtherServiceLead
        fields = [
        "location", "service_details", "timeline", "name", "phone", "email"
        ]
        widgets = {
            'timeline': DateInput(),
        }
