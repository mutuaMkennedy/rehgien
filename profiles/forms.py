from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from . import models
from leaflet.forms.widgets import LeafletWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ClearableFileInput

# referencing the custom user model
User = get_user_model()

class profile_form(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email']


    def signup(self,request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username','first_name', 'last_name','email','profile_image']

class BusinessPageEditForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorUploadingWidget(config_name='agent_profile'))
    class Meta:
        model = models.BusinessProfile
        exclude = ['user','pro_category', 'featured', 'saves','followers',
                    'member_since'
                   ]
        fields = '__all__'
        widgets = {'location':LeafletWidget()}

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = models.PortfolioItem
        exclude =  ['created_at', 'created_by']
        fields = '__all__'
        widgets = {'map_point':LeafletWidget()}

class PortfolioItemPhotoForm(forms.ModelForm):
	class Meta:
		model = models.PortfolioItemPhoto
		fields = ['photo']
		widgets = {
			'photo': ClearableFileInput(attrs={'multiple':True})
		}
