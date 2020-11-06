from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from . import models
from .models import (
                    User,
                    AgentProfile,
                    AgentReviews,
                    CompanyProfile,
                    CompanyReviews,
                    PropertyManagerProfile,
                    PropertyManagerReviews,
                    DesignAndServiceProProfile,
                    DesignAndServiceProReviews,
                    PMPortfolio,
                    PMPortfolioImages,
                    DesignAndServiceProProjects,
                    DSProProjectImages,
                    TeammateConnection,
                    )
from ckeditor.widgets import CKEditorWidget
from leaflet.admin import LeafletGeoAdmin
from embed_video.admin import AdminVideoMixin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'User Type',  # group heading of choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'user_type',
                    'profile_image',
                ),
            },
        ),
    )

class CompanyProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class CompanyTopClientInline(admin.StackedInline):
	model = models.CompanyTopClient
	extra = 3

class CompanyBusinessHoursInline(admin.StackedInline):
	model = models.CompanyBusinessHours
	extra = 1

class CompanyProfileAdmin(LeafletGeoAdmin):
    form = CompanyProfileAdminForm
    inlines = [
    CompanyTopClientInline, CompanyBusinessHoursInline
    ]

class AgentProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = AgentProfile
        fields = '__all__'

class AgentTopClientInline(admin.StackedInline):
	model = models.AgentTopClient
	extra = 3

class AgentBusinessHoursInline(admin.StackedInline):
	model = models.AgentBusinessHours
	extra = 1

class AgentProfileAdmin(LeafletGeoAdmin):
    form = AgentProfileAdminForm
    inlines = [
        AgentTopClientInline, AgentBusinessHoursInline
    ]

class PropertyManagerProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = PropertyManagerProfile
        fields = '__all__'

class PropertyManagerTopClientInline(admin.StackedInline):
	model = models.PropertyManagerTopClient
	extra = 3

class PropertyManagerBusinessHoursInline(admin.StackedInline):
	model = models.PropertyManagerBusinessHours
	extra = 1

class PropertyManagerProfileAdmin(LeafletGeoAdmin):
    form = PropertyManagerProfileAdminForm
    inlines = [
        PropertyManagerTopClientInline, PropertyManagerBusinessHoursInline
    ]

class DSProProfileAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget(config_name='agent_profile'))
    class Meta:
        model = DesignAndServiceProProfile
        fields = '__all__'

class DSTopClientInline(admin.StackedInline):
	model = models.DSTopClient
	extra = 3

class DSBusinessHoursInline(admin.StackedInline):
	model = models.DSBusinessHours
	extra = 1

class DSProProfileProfileAdmin(LeafletGeoAdmin):
    form = DSProProfileAdminForm
    inlines = [
        DSTopClientInline, DSBusinessHoursInline
    ]

class PMPortfolioImagesInline(admin.StackedInline):
	model = PMPortfolioImages
	extra = 3

class PMPortfolioAdmin(LeafletGeoAdmin):
	inlines = [PMPortfolioImagesInline]
	list_display = ("property_name","property_market_value", "property_location", "created_by")

class DSProProjectImagesInline(admin.StackedInline):
	model = DSProProjectImages
	extra = 3

class DesignAndServiceProProjectsAdmin(AdminVideoMixin,LeafletGeoAdmin):
	inlines = [DSProProjectImagesInline]
	list_display = ("project_name","project_location", "project_year", "created_by")


admin.site.register(User, CustomUserAdmin)
admin.site.register(CompanyProfile,CompanyProfileAdmin)
admin.site.register(AgentProfile,AgentProfileAdmin)
admin.site.register(PropertyManagerProfile,PropertyManagerProfileAdmin)
admin.site.register(DesignAndServiceProProfile,DSProProfileProfileAdmin)
admin.site.register(CompanyReviews)
admin.site.register(AgentReviews)
admin.site.register(PropertyManagerReviews)
admin.site.register(DesignAndServiceProReviews)
admin.site.register(PMPortfolio, PMPortfolioAdmin)
admin.site.register(DesignAndServiceProProjects, DesignAndServiceProProjectsAdmin)
admin.site.register(TeammateConnection)
