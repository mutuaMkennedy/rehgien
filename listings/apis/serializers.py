from rest_framework import serializers
from django.contrib.auth.models import User
# from listings.apis.api import MyModelResource
# from django.contrib.gis.geos import GEOSGeometry, Point
from listings.models import (
        PropertyForSale,
        RentalProperty,
        PropertyForSaleImages,
        PropertyForSaleVideos,
        RentalImages,
        RentalVideos,
                )

class UserSerializer(serializers.ModelSerializer):
    sale_property = serializers.PrimaryKeyRelatedField(many=True, queryset=PropertyForSale.objects.all())
    rent_property = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalProperty.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email','sale_property','rent_property']

class PropertyForSaleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyForSaleImages
        fields=['image']

class PropertyForSaleVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyForSaleVideos
        fields=['video']

class PropertyForSaleSerializer(serializers.ModelSerializer):
    images=PropertyForSaleImagesSerializer(many=True,read_only=True)
    videos=PropertyForSaleVideosSerializer(many=True,read_only=True)
    class Meta:
        model=PropertyForSale
        fields=[
        'id','property_name','price','type','virtual_tour_url', 'location_name',
        'location', 'thumb', 'bathrooms', 'bedrooms', 'total_rooms',
        'floor_number', 'description', 'floor_area', 'measurement_unit_choices',
        'size_units', 'number_of_units', 'number_of_stories', 'parking_spaces',
        'year_built', 'remodel_year', 'garage_sqm', 'appliances', 'basement',
        'floor_covering', 'rooms', 'indoor_features', 'cooling_type', 'heating_type',
        'heating_fuel', 'building_amenities', 'exterior', 'outdoor_amenities', 'parking',
        'roof', 'view', 'related_website', 'publishdate', 'phone', 'email',
        'images','videos',
        ]

class RentalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=RentalImages
        fields=['image']

class RentalVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model=RentalVideos
        fields=['video']

class RentalPropertySerializer(serializers.ModelSerializer):
    images=RentalImagesSerializer(many=True,read_only=True)
    videos=RentalVideosSerializer(many=True,read_only=True)
    class Meta:
        model = RentalProperty
        fields = [
                'id','property_name','type','price','virtual_tour_url', 'location_name',
                'location', 'thumb', 'bathrooms', 'bedrooms', 'total_rooms',
                'floor_number', 'description', 'floor_area', 'measurement_unit_choices',
                'size_units', 'number_of_units', 'number_of_stories', 'parking_spaces',
                'year_built', 'remodel_year', 'appliances', 'basement',
                'floor_covering', 'rooms', 'indoor_features', 'cooling_type', 'heating_type',
                'heating_fuel', 'building_amenities', 'exterior', 'outdoor_amenities', 'parking',
                'roof', 'view', 'related_website', 'publishdate','phone', 'email',
                'images','videos'
        ]
