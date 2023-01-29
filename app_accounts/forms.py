from django import forms
from phonenumber_field.formfields import PhoneNumberField

class TelInput(forms.TextInput):
	input_type = 'tel'
    
class UserPhoneNumber(forms.Form):
	phone = PhoneNumberField(widget=TelInput(attrs={'placeholder': 'Phone number'}), required=True)

class UserEmail(forms.Form):
	email = forms.EmailField(required=True)

class PhoneVerificationCode(forms.Form):
    code = forms.IntegerField(required=True)

class Password(forms.Form):
    password = forms.CharField(required=True)
