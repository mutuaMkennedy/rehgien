from django import forms
from phonenumber_field.formfields import PhoneNumberField

AGENCY_SERVICE_CHOICES = (
    ('WEB_DESIGN','web design'),
    ('BUSINESS_BRANDING','business branding'),
    ('VIDEOS_AND_ANIMATION','videos and animation'),
)

class TelInput(forms.TextInput):
	input_type = 'tel'

class ContactAgencyTeamForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your first name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your last name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your email address'}))
    phone = PhoneNumberField(widget=TelInput(attrs={'placeholder': '+254798895352'}), required=True)
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your Company Name'}))
    service_type = forms.ChoiceField(required = True, choices = AGENCY_SERVICE_CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'review_request_message'}))
