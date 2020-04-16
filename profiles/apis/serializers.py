from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth.models import User
from profiles.models import UserProfile
from listings.models import PropertyForSale, RentalProperty

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
        'pk', 'profile_image', 'phone', 'license_number', 'address',
        'facebook_link', 'twitter_link', 'linkedin_link', 'about', 'member_since',
        'account_type', 'user'
        ]

class UserSerializer(serializers.ModelSerializer):
    sale_property = serializers.PrimaryKeyRelatedField(many=True, queryset=PropertyForSale.objects.all())
    rent_property = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalProperty.objects.all())
    # user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','sale_property','rent_property', 'profile']
