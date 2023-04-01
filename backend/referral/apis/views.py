from operator import rshift
from . import serializers
from .. import models
from django.contrib.auth import get_user_model
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView,
                                    DestroyAPIView
                                    )
from rest_framework.permissions import (
                                    AllowAny,
                                    IsAuthenticated,
                                    IsAdminUser,
                                    IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q,Count
from django.shortcuts import get_object_or_404
from rest_framework import status
import uuid
import base64
from . import permissions as c_permissions

class ReferralSystemListApi(ListAPIView):
    queryset = models.ReferralSystem.objects.all()
    serializer_class = serializers.ReferralSystemSerializer

class ReferralPayoutsListApi(ListAPIView):
    serializer_class = serializers.ReferralPayoutsSerializer
    def get_queryset(self):
        """
        This view should return a list of all the Home listings
        for the currently authenticated user.
        """
        user = models.Recruiter.objects.get(recruiter=self.request.user)
        
        return models.ReferralPayouts.objects.filter(recruiter=user)


@api_view(["POST"])
def validate_referral_code(request):
    code = None
    try:
        code = str(request.data['referral_code'])
    except:
        pass

    if code != None:
        # check code is valid
        recruiter = models.Recruiter.objects.filter(referral_code=str(code))
        if recruiter.exists():
            if recruiter.first().recruiter != request.user:
                # Add user to recruiters list of referrals
                i = recruiter.first()
                i.referrals.add(request.user)
                # add payout item
                models.ReferralPayouts.objects.create(
                    recruiter = recruiter.first(),
                    amount = recruiter.first().referral_system.reward_price
                )

                message = {
                            'status': True,
                            'message':[f"Referral Code: {code} validated successfully"],
                            }

                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {
                        'status': False,
                        'message':[f"Invalid request.You cannot use your own referral code!"],
                        }

                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {
                        'status': False,
                        'message':[f"Referral Code: {code} is invalid"],
                        }

            return Response(message, status=status.HTTP_404_NOT_FOUND)
    else:
        message = {
        'referral_code': ['This field is required'],
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# def generate_verification_code():
#     return base64.urlsafe_b64encode(uuid.uuid1().bytes.encode("base64").rstrip())[:25]

# class RecruiterCreateApi(CreateAPIView):
#     queryset = models.Recruiter.objects.all()
#     serializer_class = serializers.RecruiterSerializer
#     permission_classes = [IsAuthenticated]
#     def perform_create(self,serializer):
#         referral_code = f"RGN{self.request.user.pk}" #generate_verification_code()
#         serializer.save(
#             recruiter=self.request.user,
#             referral_code = referral_code
#         )

@api_view(["POST"])
def create_recruiter_profile(request):
    if request.user.is_authenticated:
        rs = models.ReferralSystem.objects.filter(tier_name = 'TIER_TWO')
        recruiter =  models.Recruiter.objects.filter(recruiter=request.user)
        if not recruiter.exists() and rs.exists():
            referral_code = f"RGN{request.user.pk}"
            recruiter = models.Recruiter.objects.create(
                referral_system=rs.first(),
                recruiter=request.user,
                referral_code = referral_code
            )
            message = {
                        'status': True,
                        'message':[f"User created successfully"],
                        }
            
            return Response(serializers.RecruiterSerializer(recruiter).data, status=status.HTTP_201_CREATED)

        else:
            message = {
            'status': False,
            'message': ['Recruiter already exists'],
            }
            return Response(message, status=status.HTTP_409_CONFLICT)

class RecruiterUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Recruiter.objects.all()
    serializer_class = serializers.RecruiterSerializer
    permission_classes = [c_permissions.IsRecruiterOrReadOnly]