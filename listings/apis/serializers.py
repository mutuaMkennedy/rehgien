from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from listings.apis.api import MyModelResource
# from django.contrib.gis.geos import GEOSGeometry, Point
from listings import models
import datetime
from django.utils import timezone
from django.db.models import Avg, Sum
from listings.regression import trendline as trend

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


class HomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HomeType
        fields = '__all__'

class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyPhoto
        fields = ['pk','home', 'photo']

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyVideo
        fields = ['pk','home','video']

class PropertyOpenHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyOpenHouse
        fields = ["pk","home","date","start_time","end_time","reminder_list",]

class PropertyInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PropertyInteraction
        fields = ["pk","home", "user", "is_lead", "has_viewed", "views_count",
        "created_at"
        ]

class HomeSerializer(WritableNestedModelSerializer):
    home_photos= PropertyPhotoSerializer(many=True)
    home_video=PropertyVideoSerializer(many=True)
    home_interactions = PropertyInteractionSerializer(many=True)
    home_openhouse = PropertyOpenHouseSerializer(many=True)
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
    #read only method field
    _total_saves_count_ = serializers.SerializerMethodField()
    _listing_active_until_ = serializers.SerializerMethodField()
    _total_views_count_ = serializers.SerializerMethodField()
    _recent_views_count_ = serializers.SerializerMethodField()
    _views_trend_ = serializers.SerializerMethodField()
    class Meta:
        model = models.Home
        fields = [
        'HOUSE_TYPE_CHOICES','BASEMENT_CHOICES','FLOOR_COVERING_CHOICES','ROOMS_CHOICES',
        'INDOOR_FEATURES_CHOICES','COOLING_TYPE_CHOICES','HEATING_TYPE_CHOICES',
        'HEATING_FUEL_CHOICES','BUILDING_AMENITIES_CHOICES','EXTERIOR_CHOICES',
        'OUTDOOR_AMENITIES_CHOICES','PARKING_CHOICES','ROOF_CHOICES','VIEW_CHOICES',
        'APPLIANCES_CHOICES','LISTING_TYPE_CHOICES','PROPERTY_CATEGORY_CHOICES',

        'id','listing_type', 'property_category', 'property_name','price', 'home_type',
        'virtual_tour_url', 'location_name', 'location', 'bathrooms',
        'bedrooms', 'total_rooms','floor_number', 'description', 'floor_area',
        'number_of_units', 'number_of_stories', 'home_photos','home_video','home_interactions',
        'home_openhouse','saves', 'parking_spaces','year_built', 'remodel_year', 'garage_sqm','is_active',
        'deal_closed', 'final_closing_offer',

        'appliances', 'basement', 'floor_covering','rooms', 'indoor_features',
        'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities',
        'exterior', 'outdoor_amenities', 'parking', 'roof',

        'view', 'related_website', 'publishdate', 'phone', 'email','owner',
        #read only method fields
        '_total_saves_count_','_listing_active_until_','_total_views_count_', '_recent_views_count_',
        '_views_trend_',
        ]

    def get__total_saves_count_(self, obj):
        return obj.saves.count()

    def get__listing_active_until_(self, obj):
        return  obj.publishdate + datetime.timedelta(days = 30 )

    def get__total_views_count_(self, obj):
        count = obj.home_interactions.all().aggregate(Sum('views_count')).get('views_count__sum', 0)
        if count == None:
            return 0
        else:
            return count

    def get__recent_views_count_(self, obj):
        count = obj.home_interactions.filter(created_at__gte =  timezone.now() - datetime.timedelta(hours = 24) )\
				.aggregate(Sum('views_count')).get('views_count__sum', 0)
        if count == None:
            return 0
        else:
            return count

    def get__views_trend_(self, obj):
        tt_views_array = []
        for n_days in range(0,25): # in the last 24 hours
            total_views = obj.home_interactions.filter(created_at__gte = timezone.now() - datetime.timedelta(hours = n_days) )\
                         .aggregate(Sum('views_count')).get('views_count__sum', 0)
            if total_views == None:
                total_views = 0
            tt_views_array.append(total_views)
        views_index = list(range(1,len(tt_views_array)+1 ) )
        trend_line = trend(views_index,tt_views_array)
        return trend_line

class HomeSerializer2(WritableNestedModelSerializer):
    home_interactions = PropertyInteractionSerializer(many=True)
    home_openhouse = PropertyOpenHouseSerializer(many=True)
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
    #read only method field
    _total_saves_count_ = serializers.SerializerMethodField()
    _listing_active_until_ = serializers.SerializerMethodField()
    _total_views_count_ = serializers.SerializerMethodField()
    _recent_views_count_ = serializers.SerializerMethodField()
    _views_trend_ = serializers.SerializerMethodField()
    class Meta:
        model = models.Home
        fields = [
        'HOUSE_TYPE_CHOICES','BASEMENT_CHOICES','FLOOR_COVERING_CHOICES','ROOMS_CHOICES',
        'INDOOR_FEATURES_CHOICES','COOLING_TYPE_CHOICES','HEATING_TYPE_CHOICES',
        'HEATING_FUEL_CHOICES','BUILDING_AMENITIES_CHOICES','EXTERIOR_CHOICES',
        'OUTDOOR_AMENITIES_CHOICES','PARKING_CHOICES','ROOF_CHOICES','VIEW_CHOICES',
        'APPLIANCES_CHOICES','LISTING_TYPE_CHOICES','PROPERTY_CATEGORY_CHOICES',

        'id','listing_type', 'property_category', 'property_name','price', 'home_type',
        'virtual_tour_url', 'location_name', 'location', 'bathrooms',
        'bedrooms', 'total_rooms','floor_number', 'description', 'floor_area',
        'number_of_units', 'number_of_stories', 'home_photos','home_video','home_interactions',
        'home_openhouse','saves', 'parking_spaces','year_built', 'remodel_year', 'garage_sqm','is_active',
        'deal_closed', 'final_closing_offer',

        'appliances', 'basement', 'floor_covering','rooms', 'indoor_features',
        'cooling_type', 'heating_type', 'heating_fuel', 'building_amenities',
        'exterior', 'outdoor_amenities', 'parking', 'roof',

        'view', 'related_website', 'publishdate', 'phone', 'email','owner',
        #read only method fields
        '_total_saves_count_','_listing_active_until_','_total_views_count_', '_recent_views_count_',
        '_views_trend_',
        ]

    def get__total_saves_count_(self, obj):
        return obj.saves.count()

    def get__listing_active_until_(self, obj):
        return  obj.publishdate + datetime.timedelta(days = 30 )

    def get__total_views_count_(self, obj):
        count = obj.home_interactions.all().aggregate(Sum('views_count')).get('views_count__sum', 0)
        if count == None:
            return 0
        else:
            return count

    def get__recent_views_count_(self, obj):
        count = obj.home_interactions.filter(created_at__gte =  timezone.now() - datetime.timedelta(hours = 24) )\
				.aggregate(Sum('views_count')).get('views_count__sum', 0)
        if count == None:
            return 0
        else:
            return count

    def get__views_trend_(self, obj):
        tt_views_array = []
        for n_days in range(0,25): # in the last 24 hours
            total_views = obj.home_interactions.filter(created_at__gte = timezone.now() - datetime.timedelta(hours = n_days) )\
                         .aggregate(Sum('views_count')).get('views_count__sum', 0)
            if total_views == None:
                total_views = 0
            tt_views_array.append(total_views)
        views_index = list(range(1,len(tt_views_array)+1 ) )
        trend_line = trend(views_index,tt_views_array)
        return trend_line


class HomeSavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Home
        fields = ['saves']
