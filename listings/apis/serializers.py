from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
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
        fields = ['id', 'username', 'first_name', 'last_name', 'email','sale_property','rent_property']

class PropertyForSaleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyForSaleImages
        fields=['image']

class PropertyForSaleVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyForSaleVideos
        fields=['video']

class PropertyForSaleSerializer(WritableNestedModelSerializer):
    images= PropertyForSaleImagesSerializer(many=True)
    videos=PropertyForSaleVideosSerializer(many=True)
    listing_type = serializers.CharField(default='For Sale', required=False)
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
        'images','videos', 'listing_type', 'owner'
        ]

    # def create(self, validated_data):
    #     images_data = validated_data.pop('images')
    #     video_data= validated_data.pop('videos')
    #     property = PropertyForSale.objects.create(**validated_data)
    #     for images_data in images_data:
    #         PropertyForSaleImages.objects.create(property=property, **images_data)
    #     for video_data in video_data:
    #         PropertyForSaleVideos.objects.create(property=property, **video_data)
    #     return property

    # def update(self, instance, validated_data):
    #     # images_data= validated_data.pop('images')
    #     instance.images=validated_data.get('images',instance.images)
    #     instance.save()
    #     return instance

class RentalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=RentalImages
        fields=['image']

class RentalVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model=RentalVideos
        fields=['video']

class RentalPropertySerializer(WritableNestedModelSerializer):
    images=RentalImagesSerializer(many=True)
    videos=RentalVideosSerializer(many=True)
    listing_type = serializers.CharField(default='For Rent', required=False)
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
                'images','videos', 'listing_type','owner'
        ]

    # def create(self, validated_data):
    #     images_data = validated_data.pop('images')
    #     video_data= validated_data.pop('videos')
    #     property = RentalProperty.objects.create(**validated_data)
    #     for images_data in images_data:
    #         RentalImages.objects.create(property=property, **images_data)
    #     for video_data in video_data:
    #         RentalVideos.objects.create(property=property, **video_data)
    #     return property
