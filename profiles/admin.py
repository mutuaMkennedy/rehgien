from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import (
                    User,
                    NormalUserProfile,
                    AgentProfile,
                    AgentReviews,
                    PropertyManagerProfile,
                    PropertyManagerReviews,
                    DesignAndServiceProProfile,
                    DesignAndServiceProReviews
                    )
from ckeditor.widgets import CKEditorWidget
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'User Type',  # group heading of choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'user_type',
                ),
            },
        ),
    )

class AgentProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = AgentProfile
        fields = '__all__'

class AgentProfileAdmin(LeafletGeoAdmin):
    form = AgentProfileAdminForm

class PropertyManagerProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = PropertyManagerProfile
        fields = '__all__'

class PropertyManagerProfileAdmin(LeafletGeoAdmin):
    form = PropertyManagerProfileAdminForm

class DSProProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = DesignAndServiceProProfile
        fields = '__all__'

class DSProProfileProfileAdmin(LeafletGeoAdmin):
    form = DSProProfileAdminForm

admin.site.register(User, CustomUserAdmin)
admin.site.register(NormalUserProfile)
admin.site.register(AgentProfile,AgentProfileAdmin)
admin.site.register(PropertyManagerProfile,PropertyManagerProfileAdmin)
admin.site.register(DesignAndServiceProProfile,DSProProfileProfileAdmin)
admin.site.register(AgentReviews)
admin.site.register(PropertyManagerReviews)
admin.site.register(DesignAndServiceProReviews)
