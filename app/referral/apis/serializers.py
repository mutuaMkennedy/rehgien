from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
from .. import models

# referencing the custom user model
User = get_user_model()

class ReferralSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferralSystem
        fields = ['pk', "tier_name", "reward_price", "second_reward_price", "description", "active"]


class RecruiterSerializer(serializers.ModelSerializer):
    referral_system = ReferralSystemSerializer(many=False, read_only=True)
    payouts = serializers.SerializerMethodField()
    class Meta:
        model = models.Recruiter
        fields = ['pk', "referral_system", "recruiter", "referral_code", "phone_number", "referrals",
        "payouts"
        ]

    def get_payouts(self, object):
        payouts = object.recruiter_payout.all()
        return ReferralPayoutsSerializer(payouts,many=True).data


class ReferralPayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferralPayouts
        fields = ['pk', "recruiter", "amount", "is_paid"]