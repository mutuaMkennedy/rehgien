from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from listings.apis.api import MyModelResource
# from django.contrib.gis.geos import GEOSGeometry, Point
from listings import models

# referencing the custom user model
User = get_user_model()

# Lists for multiple choice fields
APPLIANCES_CHOICES = (
            ('DISH', 'Dishwasher'), ('GARB', 'Garbage disposal'),
            ('OVEN', 'Oven'), ('REFRIG', 'Refrigerator'),
            ('NON', 'None')
)

BASEMENT_CHOICES = (
        ('FINI', 'Finished'), ('UNFI', 'Unfinished'),
        ('PART', 'Partially finished'), ('NON', 'None'),
)

FLOOR_COVERING_CHOICES  = (
            ('CARP', 'Carpet'), ('CONC', 'Concrete'), ('HARD', 'Hardwood'),
            ('TILE', 'Tile'), ('SOFT', 'SoftWood'), ('OTH', 'Other'),
)

ROOMS_CHOICES = (
        ('BREA', 'BreakFast nook'), ('DINI', 'Dining room'), ('FAMI', 'Family room'),
        ('LIBR', 'Library'), ('MAST', 'Master bath'), ('MUDR', 'Mud room'),
        ('OF', 'Office'), ('PANT', 'Pantry'), ('RECR', 'Recreation room'),
        ('WORK', 'Workshop'), ('So/AR', 'Solarium/Atrium'), ('SUNR', 'Sun room'),
        ('WALK', 'walk-in-closet'),
)

INDOOR_FEATURES_CHOICES = (
                ('ATTI', 'Attic'), ('CEIL', 'Ceiling fans'),
                ('DOUB', 'Double pane windows'), ('FIRE', 'Fireplace'),
                ('SECU', 'Security system'), ('SKYL', 'Skylights'),
                ('VAUL', 'Vaulted ceiling'),
)

COOLING_TYPE_CHOICES = (
            ('CENT', 'Central'), ('EVAP', 'Evaporative'),
            ('GEOT', 'Geothermal'), ('REFR', 'Refrigeration'),
            ('SOLA', 'Solar'), ('WALL', 'Wall'),
            ('OTHE', 'Other'), ('NON', 'None'),
)

HEATING_TYPE_CHOICES = (
            ('BASE', 'Baseboard'), ('FORC', 'Forced air'),
            ('GEOT', 'Geothermal'), ('HEAT', 'Heat pump'),
            ('RADI', 'Radiant'), ('STOV', 'Stove'),
            ('WALL', 'Wall'), ('OTH', 'Other'),
)

HEATING_FUEL_CHOICES = (
            ('COAL', 'Coal'), ('ELEC', 'Electric'),
            ('GAS', 'Gas'), ('OIL', 'Oil'),
            ('PR/BU', 'Propane/Butane'), ('SOLA', 'Solar'),
            ('WO/PE', 'Wood/Pelet'), ('OTH', 'Other'),
            ('NON', 'None'),
)

BUILDING_AMENITIES_CHOICES = (
                ('BASK', 'Basketball court'), ('CONT', 'Controlled access'),
                ('DISA', 'Disabled access'), ('DOOR', 'Doorman'),
                ('ELEV', 'Elevator'), ('FITN', 'Fitness Center'),
                ('GATE', 'Gated entry'), ('NEAR', 'Near Transportation'),
                ('SPOR', 'Sports court'),
)

EXTERIOR_CHOICES = (
        ('BRIC', 'Brick'), ('CE/CO', 'Cement/Concrete'),
        ('STON', 'Stone'), ('VINY', 'Vinyl'),
        ('WOOD', 'Wood'), ('OTH', 'Other'),
)

OUTDOOR_AMENITIES_CHOICES = (
            ('BALC', 'Balcony'), ('FENC', 'Fenced yard'),
            ('GARD', 'Garden'), ('GREEN', 'Greenhouse'),
            ('LAWN', 'Lawn'), ('POND', 'Pond'),
            ('POOL', 'Pool'), ('SAUN', 'Sauna'),
            ('SPRI', 'Sprinkler system'), ('wATER', 'Waterfront'),
)

PARKING_CHOICES = (
            ('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
            ('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
            ('ONST', 'On-street'), ('NON', 'None'),
)

ROOF_CHOICES = (
        ('ASPH', 'Asphalt'), ('TILE', 'Tile'),
        ('SLAT', 'Slate'), ('OTH', 'Other'),
)

VIEW_CHOICES = (
        ('CITY', 'City'), ('TERR', 'Territorial'),
        ('MOUN', 'Mountain'), ('WATE', 'Water'),
        ('PARK', 'Park'), ('NON', 'None'),
)


class PropertyTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyTypeImage
        fields = '__all__'

class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyPhoto
        fields = ['photo']

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyVideo
        fields = ['video']

class HomeSerializer(WritableNestedModelSerializer):
    home_photos= PropertyPhotoSerializer(many=True)
    home_video=PropertyVideoSerializer(many=True)
    cooling_type = serializers.MultipleChoiceField(choices=COOLING_TYPE_CHOICES, required=False)
    appliances = serializers.MultipleChoiceField(choices=APPLIANCES_CHOICES, required=False)
    floor_covering = serializers.MultipleChoiceField(choices=FLOOR_COVERING_CHOICES, required=False)
    rooms = serializers.MultipleChoiceField(choices=ROOMS_CHOICES, required=False)
    indoor_features = serializers.MultipleChoiceField(choices=INDOOR_FEATURES_CHOICES, required=False)
    heating_type = serializers.MultipleChoiceField(choices=HEATING_TYPE_CHOICES, required=False)
    heating_fuel = serializers.MultipleChoiceField(choices=HEATING_FUEL_CHOICES, required=False)
    building_amenities = serializers.MultipleChoiceField(choices=BUILDING_AMENITIES_CHOICES, required=False)
    exterior = serializers.MultipleChoiceField(choices=EXTERIOR_CHOICES, required=False)
    outdoor_amenities = serializers.MultipleChoiceField(choices=OUTDOOR_AMENITIES_CHOICES, required=False)
    parking = serializers.MultipleChoiceField(choices=PARKING_CHOICES, required=False)
    roof = serializers.MultipleChoiceField(choices=ROOF_CHOICES, required=False)
    view = serializers.MultipleChoiceField(choices=VIEW_CHOICES, required=False)
    class Meta:
        model = models.Home
        fields = [
        'HOUSE_TYPE_CHOICES','BASEMENT_CHOICES','FLOOR_COVERING_CHOICES','ROOMS_CHOICES',
        'INDOOR_FEATURES_CHOICES','COOLING_TYPE_CHOICES','HEATING_TYPE_CHOICES',
        'HEATING_FUEL_CHOICES','BUILDING_AMENITIES_CHOICES','EXTERIOR_CHOICES',
        'OUTDOOR_AMENITIES_CHOICES','PARKING_CHOICES','ROOF_CHOICES','VIEW_CHOICES',
        'APPLIANCES_CHOICES','LISTING_TYPE_CHOICES','PROPERTY_CATEGORY_CHOICES',

        'id','listing_type', 'property_category', 'property_name','price','type',
        'virtual_tour_url', 'location_name', 'location', 'bathrooms',
        'bedrooms', 'total_rooms','floor_number', 'description', 'floor_area',
        'number_of_units', 'number_of_stories', 'home_photos','home_video','saves',
        'parking_spaces','year_built', 'remodel_year', 'garage_sqm',

        'appliances', 'basement', 'floor_covering','rooms', 'indoor_features',
        'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities',
        'exterior', 'outdoor_amenities', 'parking', 'roof',

        'view', 'related_website', 'publishdate', 'phone', 'email','owner'
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

class HomeSavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Home
        fields = ['saves']
