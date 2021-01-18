from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from phonenumber_field.formfields import PhoneNumberField
from django_select2 import forms as s2forms
from . import models

class ProCategoryWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "category_name__icontains",
    ]

class TelInput(forms.TextInput):
	input_type = 'tel'

class ProInfo(forms.ModelForm):
	business_name = forms.CharField(max_length=25, required = True)
	business_email = forms.EmailField(required = True)
	phone = PhoneNumberField(widget=TelInput(attrs={'placeholder': 'Provide a phone number that clients will use to reach you'}))
	class Meta:
		model = models.BusinessProfile
		fields = [
		'business_name','professional_category','phone',
		'business_email'
		]
		widgets = {
			'business_name': forms.TextInput(attrs={'placeholder': 'Enter your business name here'}),
			'business_email': forms.EmailInput(attrs={'placeholder': 'Enter a valid business email here'}),
			'professional_category': ProCategoryWidget,
		}

class ProServices(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'professional_services'
		]

class ProLocation(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'address','service_areas'
		]

class ProBusinessProfileImage(forms.ModelForm):
	business_profile_image = forms.ImageField(widget=forms.FileInput)
	class Meta:
		model = models.BusinessProfile
		fields = [
		'business_profile_image'
		]

class ProReviewers(forms.ModelForm):
	email = SimpleArrayField(forms.EmailField( required = True))
