from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from . import models
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

class BusinessProfileAdminForm(forms.ModelForm):
    class Meta:
        model = models.BusinessProfile
        fields = '__all__'

class ClientInline(admin.StackedInline):
	model = models.Client
	extra = 3

class BusinessHoursInline(admin.StackedInline):
	model = models.BusinessHours
	extra = 1

class ReviewInline(admin.StackedInline):
	model = models.Review
	extra = 1

class BusinessProfileAdmin(LeafletGeoAdmin):
    form = BusinessProfileAdminForm
    inlines = [
    ClientInline, BusinessHoursInline,ReviewInline
    ]

class PortfolioItemPhotoInline(admin.StackedInline):
	model = models.PortfolioItemPhoto
	extra = 3

class PortfolioItemAdmin(AdminVideoMixin,LeafletGeoAdmin):
	inlines = [PortfolioItemPhotoInline]
	list_display = ("name","worth", "address", "created_by")



admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.BusinessProfile,BusinessProfileAdmin)
admin.site.register(models.PortfolioItem, PortfolioItemAdmin)
admin.site.register(models.TeammateConnection)
