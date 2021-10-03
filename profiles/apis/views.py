from . import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models
from rest_framework import filters
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView,
                                    DestroyAPIView
                                    )
from rest_framework.views import APIView
from .permissions import (
                        IsUserOrReadOnly,IsOwnerOrReadOnly,AccountOwnerOrReadOnly,
                        IsAPro,IsRequestorOrReceiver,IsProfileOwnerOrReadOnly,
                        IsBusinessProfileOwnerOrReadOnly, IsPtfOwnerOrReadOnly
                        )
from rest_framework.permissions import (
                                    AllowAny,
                                    IsAuthenticated,
                                    IsAdminUser,
                                    IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response
import django_filters
from rest_framework.decorators import api_view
from .utils import otp_generator
from .africas_talking import send_otp_sms
import django_filters
import re


# referencing the custom user model
User = get_user_model()

"""
Phone OTP send and validation views start here
"""
def send_otp(phone_number):
    """
        Helper function for generating and sending otp code to user's phone.
    """

    if phone_number:
        otp_code = otp_generator()
        phone = str(phone_number)
        try:
            #send code to phone Number
            sms = send_otp_sms(otp_code)
            if sms == True:
                return str(otp_code) # that we will store in the db for later validation when the user sends the code for verification
            else:
                return False
        except Exception as e:
            print(e)
            return False

def check_otp_count(phone_number):
    old_otp = models.PhoneOTP.objects.filter(phone__exact = phone_number)
    if old_otp.exists():
        if old_otp.first().count > 7:
            message = {'status': False, 'detail': 'Maximum OTP code requests reached. Contact customer support.'}
            return message
        else:
            return True
    else:
        return True

@api_view(['POST'])
def validate_phone_send_otp(request):
    phone_number = ''
    try:
        phone_number = str(request.data['phone'])
    except:
        pass
    #check if phone number exist in the request
    if phone_number:
        user_obj = User.objects.filter(phone__iexact = phone_number)
        if user_obj.exists(): #check if user exist
            return Response({'status': False, 'detail': 'User with that phone number already exists.'})
        else:
            otp_count_check_status = check_otp_count(phone_number)
            if otp_count_check_status == True: # if true, meaning check passed, continue with the rest of the program
                otp_code = send_otp(phone_number)
                if otp_code != False:
                    """
                    Checking whether otp code object exists before we create a new one.
                    If exists increase the count if not create the otp object
                    """
                    old_otp = ''
                    try:
                        old_otp = models.PhoneOTP.objects.get(phone__exact = phone_number)
                    except:
                        pass
                    if old_otp:
                        ins_count = old_otp.count
                        old_otp.count = ins_count + 1 # Increase the count
                        old_otp.otp = otp_code # Update the old otp with the new otp code
                        old_otp.save(update_fields=['count','otp'])
                    else:
                        models.PhoneOTP.objects.create(
                            phone = phone_number,
                            otp = otp_code,
                            count = 1
                        )

                    return Response({'status':True, 'detail': 'OTP code sent succesfully.'})
                else:
                    return Response({'status': False, 'detail':'OTP code not sent. Try again later.'})
            else: # Check failed and user has maxed out 7 otp requests allowed.
                return Response(otp_count_check_status)
    else:
        return Response({'phone':'Phone number is required e.g. +254xxxxxxxxx'})

@api_view(['POST'])
def validate_sent_otp(request):
    phone_number = ''
    otp_code = ''
    try:
        phone_number = str(request.data['phone'])
        otp_code = str(request.data['otp'])
    except:
        pass

    if phone_number and otp_code:
        otp_instance = ''
        try:
            otp_instance = models.PhoneOTP.objects.get(phone__iexact=phone_number)
        except:
            pass
        if otp_instance:
            if otp_instance.logged == False:
                otp_instance.logged = True
                otp_instance.save( update_fields=['logged'])
                return Response({'status': True, 'detail':'Phone number sucessfully verified.'})
            else:
                return Response({'status': True, 'detail':'Phone number alredy verified.'})
        else:
            return Response({'status': False, 'detail':'OTP code provided does not match. Make sure you entered the correct code or request another code.'})
    else:
        return Response({'phone':'Field is required','otp':'Field is required'})

"""
Phone OTP send and validation views end here
"""
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'^\+?1?\d{9,14}$'
@api_view(['GET'])
def lookup_user_obj_for_login(request):
    """
    This function check whether a user exists in the db then sends that users
    username which the client app can use to automatically login the user.
    """
    q = request.GET.get('email_or_phone', '')
    if re.fullmatch(email_regex, q):
        user_obj = User.objects.filter(email__iexact=q)
        response_obj = ''
        if user_obj.exists():
            response_obj = {
            'status': True,
            'user':{
                'pk':user_obj.first().pk,
                'username':user_obj.first().username,
                }
            }
        else:
            response_obj = {'status': False, 'detail':'User not found. Make sure you entered the correct email.'}
        return Response(response_obj)
    elif re.fullmatch(phone_regex,q):
        user_obj = User.objects.filter(phone__iexact=q)
        response_obj = ''
        if user_obj.exists():
            response_obj = {
            'status': True,
            'user':{
                'pk':user_obj.first().pk,
                'username':user_obj.first().username,
                }
            }
        else:
            response_obj = {'status': False, 'detail':'User not found. Make sure you entered the correct phone number.'}
        return Response(response_obj)
    else:
        return Response({'status':False, 'detail':'Email or Phone number you provided is invalid.'})


class UserAccountsFilter(django_filters.FilterSet):
    email = django_filters.rest_framework.CharFilter(field_name="email", lookup_expr='iexact')
    phone = django_filters.rest_framework.CharFilter(field_name="phone", lookup_expr='icontains')
    class Meta:
        model = User
        fields = {
            'email', 'phone',
        }

class UsersListAPI(ListAPIView):
    serializer_class = serializers.UserAccountSerializer
    queryset = User.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = UserAccountsFilter

class UsersAccountRetrieve(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserAccountSerializer

class UserAccountEditApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserAccountSerializer
    permission_classes = [AccountOwnerOrReadOnly]

class UserListingsListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class ProfessionalGroupListApi(ListAPIView):
    queryset = models.ProfessionalGroup.objects.all()
    serializer_class = serializers.ProfessionalGroupSerializer

class ProfessionalCategoryListApi(ListAPIView):
    queryset = models.ProfessionalCategory.objects.all()
    serializer_class = serializers.ProfessionalCategorySerializer

class ProfessionalServiceListApi(ListAPIView):
    queryset = models.ProfessionalService.objects.all()
    serializer_class = serializers.ProfessionalServiceSerializer

#Busines profile
class BusinessProfileFilter(django_filters.FilterSet):
    address = django_filters.rest_framework.CharFilter(field_name="address", lookup_expr='icontains')
    professional_category = django_filters.rest_framework.CharFilter(field_name="professional_category__category_name", lookup_expr='icontains')
    professional_services = django_filters.rest_framework.CharFilter(field_name="professional_services__service_name", lookup_expr='icontains')
    service_areas = django_filters.rest_framework.CharFilter(field_name="service_areas__town_name", lookup_expr='icontains')
    class Meta:
        model = models.BusinessProfile
        fields = {
            'address','service_areas', 'professional_category', 'professional_services',
        }

class BusinessProfileListApi(ListAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = BusinessProfileFilter
    ordering_fields  = ['saves','followers']

class BusinessProfileDetailApi(RetrieveAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer

class BusinessProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

class SocialBusinessProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.SocialBusinessProfileSerializer
    permission_classes = [IsAuthenticated]

class ReviewListApi(ListAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

class ReviewCreateApi(CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(reviewer=self.request.user)

class LikeReviewUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.LikeReviewSerializer
    permission_classes = [IsAuthenticated]

class LikeReviewUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.LikeReviewSerializer
    permission_classes = [IsAuthenticated]

# Portfolio crud
# Uses a different serializer which does not nest portfolio photo table in the response
# which were raising issues in multi file uploads. Media files are uploaded
# with a separate api
class PortfolioItemCreateApi(CreateAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer2
    permission_classes = [IsAPro]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class PortfolioItemListApi(ListAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer

class PortfolioItemDetailApi(RetrieveAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer

# Uses a different serializer which does not nest portfolio photo table in the response
# which were raising issues in multi file uploads. Media files are uploaded
# with a separate api
class PortfolioItemUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer2
    permission_classes = [IsOwnerOrReadOnly]

class PortfolioItemDeleteApi(DestroyAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Uses a different serializer which does not nest portfolio photo table in the response
# which were raising issues in multi file uploads. Media files are uploaded
# with a separate api
class PortfolioItemPhotoCreateApi(CreateAPIView):
    queryset = models.PortfolioItemPhoto.objects.all()
    serializer_class = serializers.PortfolioItemPhotoSerializer
    permission_classes = [IsAPro]
    # def perform_create(self,serializer):
    #     serializer.save(portfolio_item.created_by=self.request.user)

class PortfolioItemPhotoListApi(ListAPIView):
    queryset = models.PortfolioItemPhoto.objects.all()
    serializer_class = serializers.PortfolioItemPhotoSerializer

class PortfolioItemPhotoDetailApi(RetrieveAPIView):
    queryset = models.PortfolioItemPhoto.objects.all()
    serializer_class = serializers.PortfolioItemPhotoSerializer

class PortfolioItemPhotoUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PortfolioItemPhoto.objects.all()
    serializer_class = serializers.PortfolioItemPhotoSerializer
    permission_classes = [IsPtfOwnerOrReadOnly]

class PortfolioItemPhotoDeleteApi(DestroyAPIView):
    queryset = models.PortfolioItemPhoto.objects.all()
    serializer_class = serializers.PortfolioItemPhotoSerializer
    permission_classes = [IsPtfOwnerOrReadOnly]

# team connection crud
class TeammateConnectionCreate(CreateAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]
    def perform_create(self,serializer):
        serializer.save(requestor=self.request.user)

class TeammateConnectionListApi(ListAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer

class TeammateConnectionDetailApi(RetrieveAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer

class TeammateConnectionUpdateApi(RetrieveUpdateAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]

class TeammateConnectionDeleteApi(DestroyAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]

# Business Hours
class BusinessHoursCreate(CreateAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsAPro]

class BusinessHoursListApi(ListAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer

class BusinessHoursDetailApi(RetrieveAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer

class BusinessHoursUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

class BusinessHoursDeleteApi(DestroyAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

# Client
class ClientCreate(CreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAPro]

class ClientListApi(ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientDetailApi(RetrieveAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

class ClientDeleteApi(DestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]
