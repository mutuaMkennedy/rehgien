from django import forms
from . import models
from leaflet.forms.widgets import LeafletWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_select2 import forms as s2forms
from location import models as location_models

class ServiceAreasWidget(s2forms.ModelSelect2MultipleWidget):
	search_fields = [
		"town_name__icontains",
	]

class BusinessProfileImage(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	width = forms.FloatField(widget=forms.HiddenInput())
	height = forms.FloatField(widget=forms.HiddenInput())
	business_profile_image = forms.ImageField(widget=forms.FileInput)
	class Meta:
		model = models.BusinessProfile
		fields = [
		'business_profile_image'
		]

		# def save(self):
		# 	photo = super(BusinessProfileImage, self).save(commit=False)
		# 	x = self.cleaned_data.get('x')
		# 	y = self.cleaned_data.get('y')
		# 	w = self.cleaned_data.get('width')
		# 	h = self.cleaned_data.get('height')
		# 	image = Image.open(photo.business_profile_image).convert('RGB')
		# 	cropped_image = image.crop((x, y, w+x, h+y))
		# 	resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		# 	resized_image.save(photo.business_profile_image.path)
		# 	return photo

class BusinessProfilePageInfo(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'business_name','phone', 'business_email','website_link', 'facebook_page_link', 'twitter_page_link',
		'linkedin_page_link', 'instagram_page_link','address', 'location',
		]
		widgets = {'location':LeafletWidget()}

class BusinessProfileAbout(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'about_video','about'
		]

class BusinessProfileServices(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'professional_services'
		]
		widgets = {
			'professional_services': s2forms.Select2MultipleWidget(attrs={'data-placeholder':'Search and select any services applicable to you.'}),
		}

class BusinessProfileServiceAreas(forms.ModelForm):
	class Meta:
		model = models.BusinessProfile
		fields = [
		'service_areas'
		]
		widgets = {
			'service_areas': ServiceAreasWidget(attrs={'data-placeholder': 'Search and select areas where you want to work from the suggestions.'}),
		}

class ClientForm(forms.ModelForm):
	client_logo = forms.ImageField(widget=forms.FileInput)
	class Meta:
		model = models.Client
		exclude = ["business_profile","created_at"]
		fields = '__all__'

class BusinessHoursForm(forms.ModelForm):
	class Meta:
		model = models.BusinessHours
		exclude=['profile']
		fields = '__all__'
