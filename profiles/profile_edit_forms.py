from django import forms
from . import models
from leaflet.forms.widgets import LeafletWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import FileInput


class AgentProfileProfileImage(forms.ModelForm):
    banner_image = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.AgentProfile
        fields = [
        'banner_image'
        ]

class AgentProfilePageInfo(forms.ModelForm):
    class Meta:
        model = models.AgentProfile
        fields = [
        'phone', 'website_link', 'facebook_link', 'twitter_link',
        'linkedin_link', 'address', 'location', 'license_number',
        ]
        widgets = {'location':LeafletWidget()}

class AgentProfileAbout(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = models.AgentProfile
        fields = [
        'about'
        ]

class AgentProfileServices(forms.ModelForm):
    speciality_choices = {
            ('1', 'Buying and Selling of houses'),
            ('2', 'Renting houses'),
            ('3', 'Leasing office spaces'),
            ('4', 'Buying and selling of land'),
        }
    speciality = forms.MultipleChoiceField(required=False, choices =speciality_choices, widget = forms.SelectMultiple())
    class Meta:
        model = models.AgentProfile
        fields = [
        'speciality'
        ]

class AgentProfileServiceAreas(forms.ModelForm):
    class Meta:
        model = models.AgentProfile
        fields = [
        'service_areas'
        ]


class CompanyProfileProfileImage(forms.ModelForm):
    banner_image = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.CompanyProfile
        fields = [
        'banner_image'
        ]

class CompanyProfilePageInfo(forms.ModelForm):
    class Meta:
        model = models.CompanyProfile
        fields = [
        'phone', 'website_link', 'facebook_link', 'twitter_link',
        'linkedin_link', 'address', 'location', 'license_number',
        ]
        widgets = {'location':LeafletWidget()}

class CompanyProfileAbout(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = models.CompanyProfile
        fields = [
        'about'
        ]

class CompanyProfileServices(forms.ModelForm):
    speciality_choices = (
        ('Property Management', 'Property Management'),
        ('Agency', 'Agency'),
        ('Consultancy', 'Consultancy')
    )
    speciality = forms.MultipleChoiceField(required=False, choices =speciality_choices, widget = forms.SelectMultiple())
    class Meta:
        model = models.CompanyProfile
        fields = [
        'speciality'
        ]

class CompanyProfileServiceAreas(forms.ModelForm):
    class Meta:
        model = models.CompanyProfile
        fields = [
        'service_areas'
        ]



class PmProfileProfileImage(forms.ModelForm):
    banner_image = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.PropertyManagerProfile
        fields = [
        'banner_image'
        ]

class PmProfilePageInfo(forms.ModelForm):
    class Meta:
        model = models.PropertyManagerProfile
        fields = [
        'phone', 'website_link', 'facebook_link', 'twitter_link',
        'linkedin_link', 'address', 'location', 'license_number',
        ]
        widgets = {'location':LeafletWidget()}

class PmProfileAbout(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = models.PropertyManagerProfile
        fields = [
        'about'
        ]

# class PmProfileServices(forms.ModelForm):
#     speciality_choices = (
#         ('Property Management', 'Property Management'),
#         ('Agency', 'Agency'),
#         ('Consultancy', 'Consultancy')
#     )
#     speciality = forms.MultipleChoiceField(required=False, choices =speciality_choices, widget = forms.SelectMultiple())
#     class Meta:
#         model = models.PropertyManagerProfile
#         fields = [
#         'speciality'
#         ]

class PmProfileServiceAreas(forms.ModelForm):
    class Meta:
        model = models.PropertyManagerProfile
        fields = [
        'service_areas'
        ]


class DSProfileProfileImage(forms.ModelForm):
    banner_image = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.DesignAndServiceProProfile
        fields = [
        'banner_image'
        ]

class DSProfilePageInfo(forms.ModelForm):
    class Meta:
        model = models.DesignAndServiceProProfile
        fields = [
        'phone', 'website_link', 'facebook_link', 'twitter_link',
        'linkedin_link', 'instagram_link', 'address', 'location',
        ]
        widgets = {'location':LeafletWidget()}

class DSProfileAbout(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = models.DesignAndServiceProProfile
        fields = [
        'about'
        ]

class DSProfileServices(forms.ModelForm):
    class Meta:
        model = models.DesignAndServiceProProfile
        fields = [
        'pro_speciality'
        ]

class DSProfileServiceAreas(forms.ModelForm):
    class Meta:
        model = models.DesignAndServiceProProfile
        fields = [
        'service_areas'
        ]

class CompanyTopClientForm(forms.ModelForm):
    client_logo = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.CompanyTopClient
        exclude = ["profile","created_at"]
        fields = '__all__'

class AgentTopClientForm(forms.ModelForm):
    client_logo = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.AgentTopClient
        exclude = ["profile","created_at"]
        fields = '__all__'

class PropertyManagerTopClientForm(forms.ModelForm):
    client_logo = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.PropertyManagerTopClient
        exclude = ["profile","created_at"]
        fields = '__all__'

class DSTopClientForm(forms.ModelForm):
    client_logo = forms.ImageField(widget=FileInput)
    class Meta:
        model = models.DSTopClient
        exclude = ["profile","created_at"]
        fields = '__all__'

class CompanyBusinessHoursForm(forms.ModelForm):
    class Meta:
        model = models.CompanyBusinessHours
        exclude=['user']
        fields = '__all__'

class AgentBusinessHoursForm(forms.ModelForm):
    class Meta:
        model = models.AgentBusinessHours
        exclude = ['user']
        fields = '__all__'

class PropertyManagerBusinessHoursForm(forms.ModelForm):
    class Meta:
        model = models.PropertyManagerBusinessHours
        exclude=['user']
        fields = '__all__'

class DSBusinessHoursForm(forms.ModelForm):
    class Meta:
        model = models.DSBusinessHours
        exclude=['user']
        fields = '__all__'
