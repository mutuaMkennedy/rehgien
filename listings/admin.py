from django.contrib import admin
from . import models
from leaflet.admin import LeafletGeoAdmin


class PropertyPhotoInline(admin.StackedInline):
	model = models.PropertyPhoto
	extra = 3

class PropertyVideoInline(admin.StackedInline):
	model = models.PropertyVideo
	extra = 0

class HomeAdmin(LeafletGeoAdmin):
	inlines = [PropertyPhotoInline,PropertyVideoInline]
	list_display = ('property_name','type','owner')

admin.site.register(models.PropertyTypeImage)
admin.site.register(models.Home, HomeAdmin)
