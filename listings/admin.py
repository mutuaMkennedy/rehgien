from django.contrib import admin
from . import models
from leaflet.admin import LeafletGeoAdmin


class PropertyPhotoInline(admin.StackedInline):
	model = models.PropertyPhoto
	extra = 3

class PropertyVideoInline(admin.StackedInline):
	model = models.PropertyVideo
	extra = 0

class PropertyOpenHouseInline(admin.StackedInline):
	model = models.PropertyOpenHouse
	extra = 0

class PropertyInteractionInline(admin.StackedInline):
	model = models.PropertyInteraction
	extra = 0

class HomeAdmin(LeafletGeoAdmin):
	inlines = [
	PropertyPhotoInline,PropertyVideoInline, PropertyInteractionInline,
	PropertyOpenHouseInline
	]
	list_display = ('property_name','home_type','owner')


admin.site.register(models.Home, HomeAdmin)
admin.site.register(models.HomeType)
admin.site.register(models.SavedSearch)
