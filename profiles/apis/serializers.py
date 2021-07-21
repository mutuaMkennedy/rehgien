from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models as profiles_models
from listings import models as listings_models
from listings.apis import serializers as listings_serializers
from location.api import serializers as location_serializers
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
    reviewer_user_object = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.Review
        fields = [
        'pk',"recommendation_rating_choices","responsive_rating_choices","knowledge_rating_choices","professionalism_rating_choices",
        "quality_rating_choices","profile","recommendation_rating","responsive_rating","knowledge_rating","professionalism_rating",
        "quality_of_service_rating","comment","likes","reviewer","review_date","reviewer_user_object"
        ]

    def get_reviewer_user_object(self,obj):
        user_object = {
            'id':obj.reviewer.pk,
            'username':obj.reviewer.username,
            'first_name':obj.reviewer.first_name,
            'last_name':obj.reviewer.last_name,
            'email':obj.reviewer.email,
            'user_type':obj.reviewer.user_type,
            'profile_image':obj.reviewer.profile_image.url if obj.reviewer.profile_image else '',
            }
        return user_object

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
    service_areas = location_serializers.KenyaTownSerializer(many=True)
    pro_portfolio_items = serializers.SerializerMethodField()
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
        "pro_portfolio_items","_pro_average_rating_","_business_profile_percentage_complete_",
        ]

    def get_pro_portfolio_items(self,obj):
        portfolio_object = profiles_models.PortfolioItem.objects.filter(created_by=obj.user.pk)
        portfolio_item_array = []
        for ptf in portfolio_object:
            ptf_object_photos = []

            # looping over all the photos related to this portfolio object
            for pic in ptf.portfolio_item_photo.all():
                photo_object = {
                    'pk':pic.pk,
                    'portfolio_item':pic.portfolio_item.pk,
                    'photo':pic.photo.url if pic.photo else '',
                }
                ptf_object_photos.append(photo_object)

            # creating the user object arrray
            user_object = {
                'id':ptf.created_by.pk,
                'username':ptf.created_by.username,
                'first_name':ptf.created_by.first_name,
                'last_name':ptf.created_by.last_name,
                'email':ptf.created_by.email,
                'user_type':ptf.created_by.user_type,
                'profile_image':ptf.created_by.profile_image.url if ptf.created_by.profile_image else '',
                }

            # and finally creating the portfolio object arrray
            portfolio_object = {
                'pk':ptf.pk,
                'name': ptf.name,
                'description': ptf.description,
                'video': ptf.video,
                'photos':ptf_object_photos,
                'created_at': ptf.created_at,
                'created_by': user_object,
             }

            portfolio_item_array.append(portfolio_object)

        return portfolio_item_array

    def get__pro_average_rating_(self,obj):
        rating = obj.pro_business_review.all().aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
        if rating:
            return rating
        else:
            return 0


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
        fields = ['pk','portfolio_item','photo']

class PortfolioItemSerializer(WritableNestedModelSerializer):
    portfolio_item_photo= PortfolioItemPhotoSerializer(many=True)
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "pk","name","description","video","portfolio_item_photo","created_at","created_by",
        ]

class PortfolioItemSerializer2(WritableNestedModelSerializer):
    class Meta:
        model = profiles_models.PortfolioItem
        fields = [
        "pk","name","description","video","created_at","created_by",
        ]

class TeammateConnectionSerializer(serializers.ModelSerializer):
    requestor_user_object = serializers.SerializerMethodField()
    receiver_user_object = serializers.SerializerMethodField()
    requestor_business_profile = serializers.SerializerMethodField()
    receiver_business_profile = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.TeammateConnection
        fields = [
        'pk',"requestor", "receiver", "accepted_choices","receiver_accepted", "starred",
        "requestor_user_object","receiver_user_object","requestor_business_profile",
        "receiver_business_profile"
        ]

    def get_requestor_user_object(self,obj):
        user_object = {
            'id':obj.requestor.pk,
            'username':obj.requestor.username,
            'first_name':obj.requestor.first_name,
            'last_name':obj.requestor.last_name,
            'email':obj.requestor.email,
            'user_type':obj.requestor.user_type,
            'profile_image':obj.requestor.profile_image.url if obj.requestor.profile_image else '',
            }
        return user_object

    def get_receiver_user_object(self,obj):
        user_object = {
            'id':obj.receiver.pk,
            'username':obj.receiver.username,
            'first_name':obj.receiver.first_name,
            'last_name':obj.receiver.last_name,
            'email':obj.receiver.email,
            'user_type':obj.receiver.user_type,
            'profile_image':obj.receiver.profile_image.url if obj.receiver.profile_image else '',
            }
        return user_object

    def get_requestor_business_profile(self, obj):
        if obj.requestor.user_type == 'PRO':
            profile = {
            "pk": obj.requestor.pro_business_profile.pk,
            "user": obj.requestor.pro_business_profile.user.username,
            "professional_category": obj.requestor.pro_business_profile.professional_category.category_name,
            "business_name": obj.requestor.pro_business_profile.business_name,
            "business_profile_image": obj.requestor.pro_business_profile.business_profile_image.url if obj.requestor.pro_business_profile.business_profile_image else ''
            }
            return profile
        else:
            return ''

    def get_receiver_business_profile(self, obj):
        if obj.receiver.user_type == 'PRO':
            profile = {
            "pk": obj.receiver.pro_business_profile.pk,
            "user": obj.receiver.pro_business_profile.user.username,
            "professional_category": obj.receiver.pro_business_profile.professional_category.category_name,
            "business_name": obj.receiver.pro_business_profile.business_name,
            "business_profile_image": obj.receiver.pro_business_profile.business_profile_image.url if obj.receiver.pro_business_profile.business_profile_image else ''
            }
            return profile
        else:
            return ''

class UserAccountSerializer(WritableNestedModelSerializer):
    pro_business_profile = BusinessProfileSerializer(many=False)
    profiles_portfolioitem_createdby_related = PortfolioItemSerializer(many=True)
    connection_requestor = TeammateConnectionSerializer(many=True)
    connection_request_receiver = TeammateConnectionSerializer(many=True)
    listings_home_owner_related = listings_serializers.HomeSerializer(many=True)
    _user_account_percentage_complete_ = serializers.SerializerMethodField()
    business_pages_following = serializers.SerializerMethodField()
    class Meta:
        model = profiles_models.User
        fields = [
        'user_type_choices','account_type_choices','pk', 'username', 'first_name',
        'last_name', 'email', 'user_type','account_type', 'profile_image', 'business_pages_following',"pro_business_profile",
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

    def get_business_pages_following(self, object):
        business_pages_following = object.business_page_followers.all()
        page_obj_array = []
        for page in business_pages_following:
            business_page_owner = {
            "pk":page.user.pk,
            "username": page.user.username,
            "first_name": page.user.first_name,
            "last_name": page.user.last_name,
            "email": page.user.email,
            "user_type": page.user.user_type,
            "account_type": page.user.account_type,
            "profile_image": page.user.profile_image.url if page.user.profile_image else '',
            }

            fields = {
            'pk':page.pk,
            'user':business_page_owner,
            'business_name':page.business_name,
            'business_profile_image':page.business_profile_image.url if page.business_profile_image else '',
            'followers':page.followers.all().values('pk'),
            'verified':page.verified
            }
            page_obj_array.append(fields)
        return page_obj_array
