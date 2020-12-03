from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models as profiles_models
from listings import models as listings_models
from listings.apis import serializers as listings_serializers

# referencing the custom user model
User = get_user_model()

#serializing usermodel + their Listings
class UserSerializer(serializers.ModelSerializer):
    listings_home_owner_related = serializers.PrimaryKeyRelatedField(many=True, queryset= listings_models.Home.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','user_type',
        'profile_image','listings_home_owner_related',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Review
        fields = [
        'pk','rating_choices','responsive_rating_choices','knowledge_rating_choices',
        'negotiation_rating_choices','professionalism_rating_choices',
        'service_choices','profile','rating','responsive_rating',
        'knowledge_rating','negotiation_rating','professionalism_rating',
        'quality_rating', 'creativity', 'attention_to_detail',
        'service','comment','date_of_service','reviewer','review_date'
        ]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Client
        fields =[
        "pk", "business_profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.BusinessHours
        fields =[
        "WEEKDAYS","pk","business_profile","weekday","from_hour","to_hour",
        ]

class BusinessProfileSerializer(WritableNestedModelSerializer):
    services = serializers.MultipleChoiceField(choices=profiles_models.BusinessProfile.PRO_SERVICES_CHOICES, required=False)
    pro_business_client = ClientSerializer(many=True)
    pro_business_hours = BusinessHoursSerializer(many=True)
    pro_business_review = ReviewSerializer(many=True)
    class Meta:
        model = profiles_models.BusinessProfile
        fields = [
        "PRO_CATEGORY_CHOICES", "PRO_SPECIALITY_CHOICES","PRO_SERVICES_CHOICES",
        "pk","user", "business_profile_image",
        "pro_category",'pro_speciality',"business_name","phone","business_email", "address",
        "website_link", "facebook_page_link", "twitter_page_link", "linkedin_page_link",
        "instagram_page_link", "location", "about_video","about", "service_areas", "services",
        "saves", "followers", "member_since", "featured","pro_business_client",
        "pro_business_hours","pro_business_review"
        ]

class PortfolioItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PortfolioItemPhoto
        fields = ['photo']

class PortfolioItemSerializer(WritableNestedModelSerializer):
    portfolio_item_photo= PortfolioItemPhotoSerializer(many=True)
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "PORTFOLIO_ITEM_TYPE_CHOICE", "PROGRESS_CHOICES", "porfolio_item_type",
        "name", "worth", "year", "description", "address", "map_point",
        "progress", "video", "portfolio_item_photo","created_at", "created_by"
        ]

class TeammateConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.TeammateConnection
        fields = [
        'pk',"requestor", "receiver", "accepted_choices","receiver_accepted", "starred"
        ]



class UserAccountSerializer(WritableNestedModelSerializer):
    pro_business_profile = BusinessProfileSerializer(many=False)
    profiles_portfolioitem_createdby_related = PortfolioItemSerializer(many=True)
    connection_requestor = TeammateConnectionSerializer(many=True)
    connection_request_receiver = TeammateConnectionSerializer(many=True)
    listings_home_owner_related = listings_serializers.HomeSerializer(many=True)
    class Meta:
        model = profiles_models.User
        fields = [
        'user_type_choices','account_type_choices','pk', 'username', 'first_name',
        'last_name', 'email', 'user_type','account_type', 'profile_image', "pro_business_profile",
        "profiles_portfolioitem_createdby_related", "connection_requestor",
        "connection_request_receiver", "listings_home_owner_related",
        ]
