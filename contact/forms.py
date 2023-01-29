from django import forms
from  . import models
from phonenumber_field.formfields import PhoneNumberField

class TelInput(forms.TextInput):
	input_type = 'tel'

class ContactUsForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your first name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your last name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your email address'}))
    phone = PhoneNumberField(widget=TelInput(attrs={'placeholder': '+254798895352'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'review_request_message'}))
