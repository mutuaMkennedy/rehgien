from rest_framework_gis.serializers import GeoFeatureModelSerializer
from listings import models

class SalePropertySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Home
        geo_field = 'location'
        fields = [
			'property_name', 'price', 'location_name','type','location',
			'bathrooms', 'bedrooms', 'floor_area', 'pk',
			'publishdate','saves'
        ]
