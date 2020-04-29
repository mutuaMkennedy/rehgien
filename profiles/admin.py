from django.contrib import admin
from django import forms
from .models import UserProfile
from ckeditor.widgets import CKEditorWidget
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class UserProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='user_profile'))
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileAdmin(LeafletGeoAdmin):
    form = UserProfileAdminForm

admin.site.register(UserProfile,UserProfileAdmin)
