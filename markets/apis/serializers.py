from rest_framework import serializers
from django.contrib.auth import get_user_model
from markets.models import (
        PropertyRequestLead,
        ProffesionalRequestLead,
        OtherServiceLead,
        AgentLeadRequest,
        AgentPropertyRequest,
                )

# referencing the custom user model
User = get_user_model()

class PropertyRequestLeadSerializer(serializers.ModelSerializer):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )

    general_features = serializers.MultipleChoiceField(choices=GENERAL_FEATURES, required=False)
    parking_choices = serializers.MultipleChoiceField(choices=PARKING_CHOICES, required=False)
    class Meta:
        model = PropertyRequestLead
        fields = [
        "PROPERTY_TYPE_CHOICES", "OWNERSHIP", "GENERAL_FEATURES", "PARKING_CHOICES",'pk',
        "property_type", "max_price", "min_price", "max_beds", "min_beds", "property_size",
        "location", "general_features", "parking_choices", "additional_details",
        "number_of_units", "ownership", "timeline", "name", "phone", "email","profile_image", "qualified",
        "active", "owner", "claimer", "referrer", "created_date", "updated_date"
        ]

class ClaimReferPropertyRequestLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyRequestLead
        fields = ["pk","claimer", "referrer"]

class ProffesionalRequestLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProffesionalRequestLead
        fields = [
        "TYPE", 'pk',"type_of_proffesional", "location", "service_details", "timeline", "name",
        "phone", "email", "qualified", "active", "owner","profile_image", "claimer", "referrer", "created_date",
        "updated_date"
        ]

class ClaimReferProRequestLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProffesionalRequestLead
        fields = ["pk","claimer", "referrer"]

class OtherServiceLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServiceLead
        fields = [
        'pk',"location", "service_details", "timeline", "name", "phone", "email",
        "profile_image", "qualified", "active", "owner", "claimer", "referrer",
        "created_date", "updated_date"
        ]

class ClaimReferOtherServiceLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServiceLead
        fields = ["pk","claimer", "referrer"]

class AgentLeadRequestSerializer(serializers.ModelSerializer):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )

    general_features = serializers.MultipleChoiceField(choices=GENERAL_FEATURES, required=False)
    parking_choices = serializers.MultipleChoiceField(choices=PARKING_CHOICES, required=False)
    class Meta:
        model = AgentLeadRequest
        fields = [
        "PROPERTY_TYPE_CHOICES", "OWNERSHIP", "GENERAL_FEATURES", "PARKING_CHOICES",
        "NEGOTIABLE_CHOICES", 'pk', "property_type", "price", "price_negotiable", "beds",
        "property_size", "location_name", "location", "general_features", "parking_choices",
        "additional_details", "market_value", "number_of_units", "ownership", "timeline",
        "name", "phone", "email", "profile_image","qualified", "active", "owner", "claimer", "referrer", "created_date",
        "updated_date"
        ]

class ClaimReferAgentLeadRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentLeadRequest
        fields = ["pk","claimer", "referrer"]

class AgentPropertyRequestSerializer(serializers.ModelSerializer):
    GENERAL_FEATURES = (
        ('FURNISHED', 'Furnished'),
        ('SERVICED', 'Serviced')
    )
    PARKING_CHOICES = (
    			('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'),
    			('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'),
    			('ONST', 'On-street'), ('NON', 'None'),
    )
    general_features = serializers.MultipleChoiceField(choices=GENERAL_FEATURES, required=False)
    parking_choices = serializers.MultipleChoiceField(choices=PARKING_CHOICES, required=False)
    class Meta:
        model = AgentPropertyRequest
        fields = [
        "PROPERTY_TYPE_CHOICES", "OWNERSHIP", "GENERAL_FEATURES", "PARKING_CHOICES",'pk',
        "property_type", "max_price", "min_price", "max_beds", "min_beds", "property_size",
        "location_name", "general_features", "parking_choices", "additional_details",
        "market_value", "number_of_units", "ownership", "timeline", "name", "phone", "email","profile_image",
        "qualified", "active", "owner", "claimer", "referrer", "created_date", "updated_date"
        ]

class ClaimReferAgentPropertyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentPropertyRequest
        fields = ["pk","claimer", "referrer"]
