from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import (
                    NormalUserProfile,
                    AgentProfile,
                    PropertyManagerProfile,
                    DesignAndServiceProProfile
                    )
from .models import AgentReviews
from leaflet.forms.widgets import LeafletWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# referencing the custom user model
User = get_user_model()

speciality_choices = {
        ('1', 'Buying and Selling of houses'),
        ('2', 'Renting houses'),
        ('3', 'Leasing office spaces'),
        ('4', 'Buying and selling of land'),
    }
class profile_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def signup(self,request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        # profile = AgentProfile()
        # profile.user = user
        # profile.first_name = self.cleaned_data['first_name']
        # profile.last_name = self.cleaned_data['last_name']
        # profile.save()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email']

class NormalUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = NormalUserProfile
        fields = '__all__'

class AgentProfileEditForm(forms.ModelForm):
    speciality = forms.MultipleChoiceField(required=False, choices =speciality_choices, widget = forms.SelectMultiple())
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = AgentProfile
        exclude = ['user','account_type', 'featured_agent']
        fields = '__all__'
        widgets = {'location':LeafletWidget()}

class PropertyManagerProfileEditForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = PropertyManagerProfile
        exclude = ['user','account_type', 'featured_agent']
        fields = '__all__'
        widgets = {'location':LeafletWidget()}

class DesignAndServiceProProfileEditForm(forms.ModelForm):
    pro_speciality = (
            ('Interior Designer', 'Interior Designer'),
            ('Architect','Architect'),
            ('Landscape architect','Landscape architect'),
            ('Home mover','Home mover'),
            ('Plumbing','Plumbing'),
            ('Photographer','Photographer'),
            )
    pro_speciality = forms.MultipleChoiceField(required=False, choices =pro_speciality, widget = forms.SelectMultiple())
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = DesignAndServiceProProfile
        exclude = ['user','account_type', 'featured_pro']
        fields = '__all__'
        widgets = {'location':LeafletWidget()}
