from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models as profiles_models
from listings import models as listings_models
from listings.apis import serializers as listings_serializers
from django.db.models import Avg

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

class ProfessionalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.ProfessionalGroup
        fields = ['pk',"group_image","slug"]

class ProfessionalCategorySerializer(serializers.ModelSerializer):
    professional_group = ProfessionalGroupSerializer(many=False, read_only=True)
    class Meta:
        model = profiles_models.ProfessionalCategory
        fields = ['pk', "category_name","category_image","slug","professional_group",]

class ProfessionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.ProfessionalService
        fields = ['pk',"service_name","service_image","slug"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Review
        fields = [
        'pk',"recommendation_rating_choices","responsive_rating_choices","knowledge_rating_choices","professionalism_rating_choices",
        "quality_rating_choices","profile","recommendation_rating","responsive_rating","knowledge_rating","professionalism_rating",
        "quality_of_service_rating","comment","likes","reviewer","review_date",
        ]

class LikeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.Review
        fields = ["likes"]

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
    professional_category = ProfessionalCategorySerializer(many=False)
    professional_services = ProfessionalServiceSerializer(many=True)
    pro_business_client = ClientSerializer(many=True)
    pro_business_hours = BusinessHoursSerializer(many=True)
    pro_business_review = ReviewSerializer(many=True)
    _pro_average_rating_ = serializers.SerializerMethodField()
    _business_profile_percentage_complete_ = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.BusinessProfile
        fields = [
        "pk","user","professional_category","professional_services","business_profile_image",
        "business_name","phone","business_email","address","location","website_link",
        "facebook_page_link","twitter_page_link","linkedin_page_link","instagram_page_link",
        "about_video","about","service_areas","saves","followers","member_since",
        "featured","verified","pro_business_client","pro_business_hours","pro_business_review",
        "_pro_average_rating_","_business_profile_percentage_complete_",
        ]

    def get__pro_average_rating_(self,obj):
        rating = obj.pro_business_review.all().aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
        if rating:
            return 0
        else:
            return rating


    def get__business_profile_percentage_complete_(self,obj):
        percent = {
        'business_profile_image': 10, 'professional_category':10, 'phone':5, 'business_email':10,
        'address':10, 'website_link':5, 'facebook_page_link': 5,
        'twitter_page_link': 5, 'linkedin_page_link':5, 'instagram_page_link':5,
        'location':10, 'about':20
        }
        total = 0
        if obj.business_profile_image:
            total += percent.get('business_profile_image', 0)
        if obj.professional_category:
            total += percent.get('professional_category', 0)
        if obj.phone:
            total += percent.get('phone', 0)
        if obj.address:
            total += percent.get('address', 0)
        if obj.business_email:
            total += percent.get('business_email', 0)
        if obj.website_link:
            total += percent.get('website_link', 0)
        if obj.facebook_page_link:
            total += percent.get('facebook_page_link', 0)
        if obj.twitter_page_link:
            total += percent.get('twitter_page_link', 0)
        if obj.linkedin_page_link:
            total += percent.get('linkedin_page_link', 0)
        if obj.instagram_page_link:
            total += percent.get('instagram_page_link', 0)
        if obj.location:
            total += percent.get('location', 0)
        if obj.about:
            total += percent.get('about', 0)
        return "%s"%(total)

class SocialBusinessProfileSerializer(WritableNestedModelSerializer):
    class Meta:
        model = profiles_models.BusinessProfile
        fields = ["saves","followers"]

class PortfolioItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PortfolioItemPhoto
        fields = ['photo']

class PortfolioItemSerializer(WritableNestedModelSerializer):
    portfolio_item_photo= PortfolioItemPhotoSerializer(many=True)
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "name","description","video","portfolio_item_photo","created_at","created_by",
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
    _user_account_percentage_complete_ = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.User
        fields = [
        'user_type_choices','account_type_choices','pk', 'username', 'first_name',
        'last_name', 'email', 'user_type','account_type', 'profile_image', "pro_business_profile",
        "profiles_portfolioitem_createdby_related", "connection_requestor",
        "connection_request_receiver", "listings_home_owner_related",'_user_account_percentage_complete_'
        ]

    def get__user_account_percentage_complete_(self,obj):
        percent = { 'username': 10, 'first_name': 15, 'last_name': 15, 'email': 20,
        'profile_image': 30, 'user_type':5,'account_type':5}
        total = 0
        if obj.username:
            total += percent.get('username', 0)
        if obj.first_name:
            total += percent.get('first_name', 0)
        if obj.last_name:
            total += percent.get('last_name', 0)
        if obj.email:
            total += percent.get('email', 0)
        if obj.profile_image:
            total += percent.get('profile_image', 0)
        return "%s"%(total)
