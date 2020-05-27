from django.contrib import admin
from .models import (
						PropertyTypeImage,
						PropertyForSale,
						PropertyForSaleImages,
						PropertyForSaleVideos,
						RentalProperty,
						RentalImages,
						RentalVideos,
						)
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class PropertyForSaleImagesInline(admin.StackedInline):
	model = PropertyForSaleImages
	extra = 3

class PropertyForSaleVideosInline(admin.StackedInline):
	model = PropertyForSaleVideos
	extra = 3

class PropertyForSaleAdmin(LeafletGeoAdmin):
	inlines = [
				PropertyForSaleImagesInline,
	 			PropertyForSaleVideosInline,
				]
	list_display = ('property_name','type','owner')

class RentalImagesInline(admin.StackedInline):
	model = RentalImages
	extra = 3

class RentalVideosInline(admin.StackedInline):
	model = RentalVideos
	extra = 3

class RentalPropertyAdmin(LeafletGeoAdmin):
	inlines = [RentalImagesInline, RentalVideosInline]
	list_display = ('property_name', 'type', 'owner')

admin.site.register(PropertyTypeImage)
admin.site.register(PropertyForSale, PropertyForSaleAdmin)
admin.site.register(RentalProperty, RentalPropertyAdmin)
