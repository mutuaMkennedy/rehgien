from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from listings.apis.api import MyModelResource
# from django.contrib.gis.geos import GEOSGeometry, Point
from listings.models import (
        PropertyTypeImage,
        PropertyForSale,
        RentalProperty,
        PropertyForSaleImages,
        PropertyForSaleVideos,
        RentalImages,
        RentalVideos,
                )

# referencing the custom user model
User = get_user_model()

#will be removed duplicate of UserSerializer in profiles app serializers
class UserSerializer(serializers.ModelSerializer):
    sale_property = serializers.PrimaryKeyRelatedField(many=True, queryset=PropertyForSale.objects.all())
    rent_property = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalProperty.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','sale_property','rent_property']

class PropertyTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyTypeImage
        fields='__all__'

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
        'id','property_name','price','HOUSE_TYPE_CHOICES', 'type','virtual_tour_url', 'location_name',
        'location', 'thumb', 'bathrooms', 'bedrooms', 'total_rooms',
        'floor_number', 'description', 'floor_area', 'measurement_unit_choices',
        'size_units', 'number_of_units', 'number_of_stories', 'parking_spaces',
        'year_built', 'remodel_year', 'garage_sqm', 'APPLIANCES_CHOICES','appliances',
        'BASEMENT_CHOICES','basement', 'FLOOR_COVERING_CHOICES', 'floor_covering',
        'ROOMS_CHOICES', 'rooms', 'INDOOR_FEATURES_CHOICES', 'indoor_features',
        'COOLING_TYPE_CHOICES', 'cooling_type', 'HEATING_TYPE_CHOICES', 'heating_type',
        'HEATING_FUEL_CHOICES', 'heating_fuel', 'BUILDING_AMENITIES_CHOICES', 'building_amenities',
        'EXTERIOR_CHOICES', 'exterior', 'OUTDOOR_AMENITIES_CHOICES', 'outdoor_amenities',
        'PARKING_CHOICES', 'parking', 'ROOF_CHOICES', 'roof', 'VIEW_CHOICES', 'view',
        'related_website', 'publishdate', 'phone', 'email',
        'images','videos', 'listing_type', 'owner','favourite'
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
        'id','property_name','price','HOUSE_TYPE_CHOICES', 'type','virtual_tour_url', 'location_name',
        'location', 'thumb', 'bathrooms', 'bedrooms', 'total_rooms',
        'floor_number', 'description', 'floor_area', 'measurement_unit_choices',
        'size_units', 'number_of_units', 'number_of_stories', 'parking_spaces',
        'year_built', 'remodel_year', 'APPLIANCES_CHOICES','appliances',
        'BASEMENT_CHOICES','basement', 'FLOOR_COVERING_CHOICES', 'floor_covering',
        'ROOMS_CHOICES', 'rooms', 'INDOOR_FEATURES_CHOICES', 'indoor_features',
        'COOLING_TYPE_CHOICES', 'cooling_type', 'HEATING_TYPE_CHOICES', 'heating_type',
        'HEATING_FUEL_CHOICES', 'heating_fuel', 'BUILDING_AMENITIES_CHOICES', 'building_amenities',
        'EXTERIOR_CHOICES', 'exterior', 'OUTDOOR_AMENITIES_CHOICES', 'outdoor_amenities',
        'PARKING_CHOICES', 'parking', 'ROOF_CHOICES', 'roof', 'VIEW_CHOICES', 'view',
        'related_website', 'publishdate', 'phone', 'email',
        'images','videos', 'listing_type', 'owner','favourite'
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
