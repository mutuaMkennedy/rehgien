from django import forms
from . import models
from leaflet.forms.widgets import LeafletWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BusinessProfileImage(forms.ModelForm):
    business_profile_image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = models.BusinessProfile
        fields = [
        'business_profile_image'
        ]

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
    services = forms.MultipleChoiceField(required=False, choices = models.BusinessProfile.PRO_SERVICES_CHOICES, widget = forms.SelectMultiple())
    class Meta:
        model = models.BusinessProfile
        fields = [
        'services'
        ]

class BusinessProfileServiceAreas(forms.ModelForm):
    class Meta:
        model = models.BusinessProfile
        fields = [
        'service_areas'
        ]


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
