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


class CompanyReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.CompanyReviews
        fields = [
        'pk','rating_choices','responsive_rating_choices','knowledge_rating_choices',
        'negotiation_rating_choices','professionalism_rating_choices',
        'service_choices','profile','rating','responsive_rating',
        'knowledge_rating','negotiation_rating','professionalism_rating',
        'service','comment','date_of_service','user','review_date'
        ]

class CompanyTopClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.CompanyTopClient
        fields =[
        "pk", "profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class CompanyBusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.CompanyBusinessHours
        fields =[
        "WEEKDAYS","pk","user","weekday","from_hour","to_hour",
        ]

class CompanyProfileSerializer(WritableNestedModelSerializer):
    speciality_choices = (
    ('Property Management', 'Property Management'),
    ('Agency', 'Agency'),
    ('Consultancy', 'Consultancy')
    )
    speciality = serializers.MultipleChoiceField(choices=speciality_choices, required=False)
    co_top_clients = CompanyTopClientSerializer(many=True)
    co_business_hours = CompanyBusinessHoursSerializer(many=True)
    company_review = CompanyReviewsSerializer(many=True)
    class Meta:
        model = profiles_models.CompanyProfile
        fields = [
        'pk',"user", "banner_image", "speciality",'speciality_choices', "phone", "license_number",
        "address", "website_link", "facebook_link", "twitter_link", "linkedin_link",
        "location", "about", "service_areas","saves", "followers", "member_since", "account_type_choices",
        "account_type","featured_business","co_top_clients","co_business_hours","company_review"
        ]


class AgentReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.AgentReviews
        fields = [
        'pk','rating_choices','responsive_rating_choices','knowledge_rating_choices',
        'negotiation_rating_choices','professionalism_rating_choices',
        'service_choices','profile','rating','responsive_rating',
        'knowledge_rating','negotiation_rating','professionalism_rating',
        'service','comment','date_of_service','user','review_date'
        ]

class AgentTopClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.AgentTopClient
        fields =[
        "pk", "profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class AgentBusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.AgentBusinessHours
        fields =[
        "WEEKDAYS","pk","user","weekday","from_hour","to_hour",
        ]

class AgentProfileSerializer(WritableNestedModelSerializer):
    speciality_choices = (
        ('1', 'Buying and Selling of houses'),
        ('2', 'Renting houses'),
        ('3', 'Leasing office spaces'),
        ('4', 'Buying and selling of land'),
    )
    speciality = serializers.MultipleChoiceField(choices=speciality_choices, required=False)
    ag_top_clients = AgentTopClientSerializer(many=True)
    ag_business_hours = AgentBusinessHoursSerializer(many=True)
    agent_review = AgentReviewsSerializer(many=True)
    class Meta:
        model = profiles_models.AgentProfile
        fields = [
        'pk','user','banner_image','phone','license_number','address','website_link',
        'facebook_link','twitter_link','linkedin_link','location','speciality_choices',
        'speciality','about','service_areas','saves','followers', 'member_since','account_type_choices','account_type',
        'featured_agent',"ag_top_clients","ag_business_hours","agent_review"
        ]


class PropertyManagerReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PropertyManagerReviews
        fields = [
            'pk','rating_choices','responsive_rating_choices','communication_rating_choices',
            'attention_to_detail_choices','service_choices','profile','rating',
            'responsive_rating','communication_rating','attention_to_detail',
            'service','comment','date_of_service',
            'user','review_date'
        ]

class PropertyManagerTopClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PropertyManagerTopClient
        fields =[
        "pk", "profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class PropertyManagerBusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PropertyManagerBusinessHours
        fields =[
        "WEEKDAYS","pk","user","weekday","from_hour","to_hour",
        ]

class PropertyManagerProfileSerializer(WritableNestedModelSerializer):
    pm_top_clients = PropertyManagerTopClientSerializer(many=True)
    pm_business_hours = PropertyManagerBusinessHoursSerializer(many=True)
    pm_review = PropertyManagerReviewsSerializer(many=True)
    class Meta:
        model = profiles_models.PropertyManagerProfile
        fields = [
        'pk','user','banner_image','phone','license_number','address','website_link',
        'facebook_link','twitter_link','linkedin_link','location','about','service_areas',
        'saves','followers','member_since','account_type_choices','account_type',
        'featured_agent',"pm_top_clients","pm_business_hours","pm_review"
        ]


class DesignAndServiceProReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.DesignAndServiceProReviews
        fields = [
            'pk','rating_choices','quality_rating_choices','creativity_choices',
            'attention_to_detail_choices','profile','rating',
            'quality_rating','creativity_rating','attention_to_detail',
            'comment','user','review_date'
        ]

class DSTopClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PropertyManagerTopClient
        fields =[
        "pk", "profile", "client_logo", "client_name", "business_category",
        "created_at"
        ]

class DSBusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PropertyManagerBusinessHours
        fields =[
        "WEEKDAYS","pk","user","weekday","from_hour","to_hour",
        ]

class DesignAndServiceProProfileSerializer(WritableNestedModelSerializer):
    ds_top_clients = DSTopClientSerializer(many=True)
    DS_business_hours = DSBusinessHoursSerializer(many=True)
    DService_review = DesignAndServiceProReviewsSerializer(many=True)

    class Meta:
        model = profiles_models.DesignAndServiceProProfile
        fields = [
        'pk','user','banner_image','phone','address','website_link','instagram_link',
        'facebook_link','twitter_link','linkedin_link','location','about', 'service_areas','saves','followers',
        'member_since','account_type_choices','account_type','pro_speciality',
        'featured_pro',"ds_top_clients","DS_business_hours","DService_review"
        ]



class PMPortfolioImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.PMPortfolioImages
        fields = ['property_image']

class PMPortfolioSerializer(WritableNestedModelSerializer):
    PM_porfolio_Images= PMPortfolioImagesSerializer(many=True)
    class Meta:
        model = profiles_models.PMPortfolio
        fields = [
        "pk", "property_name","property_market_value", "property_location", "property_map_point","current_manager_choices",
        "currently_managing","PM_porfolio_Images", "created_at", "created_by"
        ]



class DSProProjectImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.DSProProjectImages
        fields = ['project_image']

class DesignAndServiceProProjectsSerializer(WritableNestedModelSerializer):
    DS_project_Images= DSProProjectImagesSerializer(many=True)
    class Meta:
        model = profiles_models.DesignAndServiceProProjects
        fields = [
        "pk", "project_name", "project_cost", "project_description", "project_video","DS_project_Images",
        "project_location", "project_map_point", "project_year", "created_at","created_by"
        ]



class TeammateConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles_models.TeammateConnection
        fields = [
        'pk',"requestor", "receiver", "accepted_choices","receiver_accepted", "starred"
        ]



class UserAccountSerializer(WritableNestedModelSerializer):
    company_profile = CompanyProfileSerializer(many=False)
    agent_profile = AgentProfileSerializer(many=False)
    pm_profile = PropertyManagerProfileSerializer(many=False)
    DService_profile = DesignAndServiceProProfileSerializer(many=False)
    PM_portfolio_ls_creator = PMPortfolioSerializer(many=True)
    DS_project_ls_creator = DesignAndServiceProProjectsSerializer(many=True)
    join_team_requestor = TeammateConnectionSerializer(many=True)
    join_team_request_receiver = TeammateConnectionSerializer(many=True)
    listings_home_owner_related = listings_serializers.HomeSerializer(many=True)
    class Meta:
        model = User
        fields = [
        'id', 'username', 'first_name', 'last_name', 'email', 'user_type_choices',
        'user_type','profile_image', "company_profile", "agent_profile", "pm_profile",
        "DService_profile", "PM_portfolio_ls_creator", "DS_project_ls_creator",
        "join_team_requestor", "join_team_request_receiver", "listings_home_owner_related",
        ]
