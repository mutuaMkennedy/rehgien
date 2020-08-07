from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles.models import (
                            NormalUserProfile,
                            AgentProfile,
                            AgentReviews,
                            PropertyManagerProfile,
                            PropertyManagerReviews,
                            DesignAndServiceProProfile,
                            DesignAndServiceProReviews
                            )

from listings.models import PropertyForSale, RentalProperty

# referencing the custom user model
User = get_user_model()

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_type_choices','user_type']

class UserSerializer(serializers.ModelSerializer):
    sale_property = serializers.PrimaryKeyRelatedField(many=True, queryset=PropertyForSale.objects.all())
    rent_property = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalProperty.objects.all())
    # user_profile = AgentProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','user_type','sale_property','rent_property']

class NormalUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUserProfile
        fields = '__all__'

class AgentProfileSerializer(serializers.ModelSerializer):
    speciality_choices = (
        ('1', 'Buying and Selling of houses'),
        ('2', 'Renting houses'),
        ('3', 'Leasing office spaces'),
        ('4', 'Buying and selling of land'),
    )
    speciality_choices = serializers.MultipleChoiceField(choices=speciality_choices, required=False)
    class Meta:
        model = AgentProfile
        fields = [
        'pk','user','profile_image','phone','license_number','address','website_link',
        'facebook_link','twitter_link','linkedin_link','location','speciality_choices',
        'speciality','about','member_since','account_type_choices','account_type',
        'featured_agent'
        ]

class PropertyManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyManagerProfile
        fields = [
        'pk','user','profile_image','phone','license_number','address','website_link',
        'facebook_link','twitter_link','linkedin_link','location','about',
        'member_since','account_type_choices','account_type','featured_agent'
        ]

class DesignAndServiceProProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignAndServiceProProfile
        fields = [
        'pk','user','profile_image','phone','address','website_link','instagram_link',
        'facebook_link','twitter_link','linkedin_link','location','about',
        'member_since','account_type_choices','account_type','pro_speciality','pro_speciality',
        'featured_pro'
        ]

class AgentReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentReviews
        fields = [
        'pk','rating_choices','responsive_rating_choices','knowledge_rating_choices',
        'negotiation_rating_choices','professionalism_rating_choices',
        'service_choices','profile','rating','responsive_rating',
        'knowledge_rating','negotiation_rating','professionalism_rating',
        'service','comment','date_of_service','user','review_date'
        ]

class PropertyManagerReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyManagerReviews
        fields = [
            'pk','rating_choices','responsive_rating_choices','communication_rating_choices',
            'attention_to_detail_choices','service_choices','profile','rating',
            'responsive_rating','communication_rating','attention_to_detail',
            'service','comment','date_of_service',
            'user','review_date'
        ]

class DesignAndServiceProReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignAndServiceProReviews
        fields = [
            'pk','rating_choices','quality_rating_choices','creativity_choices',
            'attention_to_detail_choices','profile','rating',
            'quality_rating','creativity_rating','attention_to_detail',
            'comment','user','review_date'
        ]
