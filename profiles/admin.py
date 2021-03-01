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

class ProfessionalCategoryInline(admin.StackedInline):
	model = models.ProfessionalCategory
	extra = 1

class ProfessionalCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("category_name","slug",)

class ProfessionalGroupAdmin(admin.ModelAdmin):
    inlines = [ProfessionalCategoryInline]
    list_display = ("group_name","slug",)
    prepopulated_fields = {"slug": ("group_name",)}

class ProfessionalServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("service_name",)}
    list_display = ("service_name","slug",)

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
    list_display = ("business_name","user",)
    inlines = [
    ClientInline, BusinessHoursInline,ReviewInline
    ]

class PortfolioItemPhotoInline(admin.StackedInline):
	model = models.PortfolioItemPhoto
	extra = 3

class PortfolioItemAdmin(AdminVideoMixin,LeafletGeoAdmin):
	inlines = [PortfolioItemPhotoInline]
	list_display = ("name","created_by")



admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.ProfessionalGroup,ProfessionalGroupAdmin)
admin.site.register(models.ProfessionalCategory,ProfessionalCategoryAdmin)
admin.site.register(models.ProfessionalService,ProfessionalServiceAdmin)
admin.site.register(models.BusinessProfile,BusinessProfileAdmin)
admin.site.register(models.PortfolioItem, PortfolioItemAdmin)
admin.site.register(models.TeammateConnection)
