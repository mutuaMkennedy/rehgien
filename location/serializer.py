from rest_framework_gis.serializers import GeoFeatureModelSerializer
from listings.models import PropertyForSale, RentalProperty

class SalePropertySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PropertyForSale
        geo_field = 'location'
        fields = [
			'property_name', 'price', 'location_name','type','thumb','location',
			'bathrooms', 'bedrooms', 'floor_area', 'size_units', 'pk',
			'publishdate','favourite'
        ]
