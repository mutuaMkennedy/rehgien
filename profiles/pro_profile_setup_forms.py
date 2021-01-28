from django import forms
from PIL import Image
from django.contrib.postgres.forms import SimpleArrayField
from phonenumber_field.formfields import PhoneNumberField
from django_select2 import forms as s2forms
from . import models
from location import models as location_models

class ProCategoryWidget(s2forms.ModelSelect2Widget):
	search_fields = [
		"category_name__icontains",
	]

class ServiceAreasWidget(s2forms.ModelSelect2MultipleWidget):
	search_fields = [
		"town_name__icontains",
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
		widgets = {
			'professional_services': s2forms.Select2MultipleWidget(attrs={'data-placeholder':'Search and select any services applicable to you.'}),
		}

class ProLocation(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'address','service_areas'
		]
		widgets = {
			'service_areas': ServiceAreasWidget(attrs={'data-placeholder': 'Search and select additional areas from the suggestions.'}),
		}

class ProBusinessProfileImage(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	width = forms.FloatField(widget=forms.HiddenInput())
	height = forms.FloatField(widget=forms.HiddenInput())
	class Meta:
		model = models.BusinessProfile
		fields = [
		'business_profile_image','x','y','width','height',
		]

	# def save(self):
	# 		photo = super(ProBusinessProfileImage, self).save()
	#
	# 		x = self.cleaned_data.get('x')
	# 		y = self.cleaned_data.get('y')
	# 		w = self.cleaned_data.get('width')
	# 		h = self.cleaned_data.get('height')
	#
	# 		image = Image.open(photo.file)
	# 		cropped_image = image.crop((x, y, w+x, h+y))
	# 		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
	# 		resized_image.save(photo.file.path)
	#
	# 		return photo

class ProReviewers(forms.Form):
	email = SimpleArrayField(forms.EmailField( required = True))
	message = forms.CharField(widget=forms.Textarea(attrs={'class':'review_request_message'}))
