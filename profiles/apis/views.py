from . import serializers
# from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from profiles import models
from location import models as location_models
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
# from .africas_talking import send_otp_sms,send_password_reset_otp_sms # Remove; Replaced with twilio service
from contact.services import twilio_service
import django_filters
import re
from django.db.models import Q,Count,Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from functools import reduce
from operator import or_

# referencing the custom user model
User = get_user_model()

site_name = Site.objects.get_current().name

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
                'user_type':user_obj.first().user_type
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
                'user_type':user_obj.first().user_type
                }
            }
        else:
            response_obj = {'status': False, 'detail':'User not found. Make sure you entered the correct phone number.'}
        return Response(response_obj)
    else:
        return Response({'status':False, 'detail':'Email or Phone number you provided is invalid.'})

"""
Phone OTP send and validation views start here
"""
def send_otp(phone_number,message):
    """
        Helper function for generating and sending otp code to user's phone.
    """

    if phone_number:
        otp_code = otp_generator()
        phone = str(phone_number)
        try:
            #send code to phone Number
            message = f'{message} {otp_code}'
            sms = twilio_service.send_SMS(message, phone)
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
                otp_code = send_otp(phone_number, 'You phone number verification code is:')
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
        otp_instance = models.PhoneOTP.objects.filter(phone__iexact=phone_number, otp=otp_code)
        if otp_instance.exists():
            #We found a otp instance matching the phone number and otp provided so log/verify the phone number
            if otp_instance.first().logged == False:
                a = otp_instance.first()
                a.logged = True
                a.save( update_fields=['logged'])
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

"""
Reset password with OTP code views start here
"""
def check_if_account_exists(q):
    """
    Helper function to check whether account requesting to reset password exists
    before sending any OTP codes
    """
    if re.fullmatch(email_regex, q):
        user_obj = User.objects.filter(email__iexact=q)
        response_obj = ''
        if user_obj.exists():
            response_obj = {
            'status': True,
            'user':{
                'pk':user_obj.first().pk,
                'username':user_obj.first().username,
                'user_type':user_obj.first().user_type
                }
            }
        else:
            response_obj = {'status': False, 'detail':'We could not find an account associated with the email you provided. Check your email and try again!'}
        return(response_obj)
    elif re.fullmatch(phone_regex,q):
        user_obj = User.objects.filter(phone__iexact=q)
        response_obj = ''
        if user_obj.exists():
            response_obj = {
            'status': True,
            'user':{
                'pk':user_obj.first().pk,
                'username':user_obj.first().username,
                'user_type':user_obj.first().user_type
                }
            }
        else:
            response_obj = {'status': False, 'detail':'We could not find an account associated with the phone number you provided. Check your phone number and try again!'}
        return(response_obj)
    else:
        return ({'status':False, 'detail':'Email or Phone number you provided is invalid.'})

def send_passcode_email(otp_code,contact_name,recepient_email):
    """
    Helper function for sending OTP to user's email
    """
    try:
        subject = f"{otp_code} is your {site_name} account recovery code."
        plainMessage = f'Hi {contact_name},\n\nWe received a request to reset your {site_name} password.\nEnter the following password reset code:\n{otp_code}.'
        context = {
        "message":plainMessage
        }

        htmlMessage = render_to_string('profiles/account_email/password_reset_with_code.html', context)

        message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [recepient_email])
        message.attach_alternative(htmlMessage, "text/html")
        message.send()
        return True

    except BadHeaderError as e:
        return({'status':True, 'detail':f'OTP not sent to {recepient_email}: {e}'})

@api_view(['POST'])
def send_otp_to_email_or_phone(request):
    """
    Function that will send otp code to user's phone or email.
    """
    q = ''
    try:
        q = str(request.data['email_or_phone'])
    except:
        pass

    if q:
        account_exists = check_if_account_exists(q) # check if account exists matching the provided detailos
        if account_exists['status'] == True:
            otp_code = otp_generator()
            # check if q is an email address or phone number to determine where to send OTP
            if re.fullmatch(phone_regex, q):

                phone_number = str(q)
                #send code to phone Number
                sms = send_otp(phone_number, 'You password reset code is:')
                if sms == True:
                    # Logging the otp code in the db
                    old_otp = ''
                    try:
                        old_otp = models.ResetPasswordOTP.objects.get(phone__exact=phone_number)
                    except:
                        pass

                    if old_otp:
                        ins_count = old_otp.count
                        old_otp.count = ins_count + 1
                        old_otp.otp = otp_code
                        old_otp.save(update_fields=['count','otp'])
                    else:
                        instance = models.ResetPasswordOTP.objects.create(
                            phone = phone_number,
                            otp = otp_code,
                            count = 1
                        )

                    return Response({'status':True, 'user':account_exists['user']})
                else:
                    sms_send_error = sms
                    return Response(sms_send_error)

            elif re.fullmatch(email_regex, q):
                recepient_email = q
                contact_name = account_exists['user']['username']
                email_sent = send_passcode_email(otp_code,contact_name,recepient_email)

                if email_sent == True:
                        # Logging the otp code in the db
                        old_otp = ''
                        try:
                            old_otp = models.ResetPasswordOTP.objects.get(email__exact=recepient_email)
                        except:
                            pass

                        if old_otp:
                            ins_count = old_otp.count
                            old_otp.count = ins_count + 1
                            old_otp.otp = otp_code
                            old_otp.save(update_fields=['count','otp'])
                        else:
                            instance = models.ResetPasswordOTP.objects.create(
                                email = recepient_email,
                                otp = otp_code,
                                count = 1
                            )

                        return Response({'status':True, 'user':account_exists['user']})
                else:
                    error = email_sent
                    return Response(error)

        else:
            return Response({'status':False, 'detail':account_exists['detail']})
    else:
        return Response({'email_or_phone': 'This field is required.'})

@api_view(['POST'])
def verify_password_reset_otp(request):
    otp_code = ''
    email_or_phone = ''
    try:
        otp_code = str(request.data['otp'])
        email_or_phone = str(request.data['email_or_phone'])
    except:
        pass
    if otp_code and email_or_phone:
        account = check_if_account_exists(email_or_phone)
        if account['status'] == True:
            if re.fullmatch(phone_regex, email_or_phone): #if its a valid phone number
                phone_number = str(email_or_phone)
                otp_obj = models.ResetPasswordOTP.objects.filter(otp = otp_code, phone = phone_number)
                if otp_obj.exists():
                    # otp code provided is correct so verify it
                    a = otp_obj.first()
                    a.verified = True
                    a.save()

                    return Response({'status':True, 'detail':'OTP sucesfully verified', 'user':account['user']})
                else:
                    return Response({'status':False, 'detail':'Invalid OTP.'})

            elif re.fullmatch(email_regex, email_or_phone):
                email_adr = str(email_or_phone)
                otp_obj = models.ResetPasswordOTP.objects.filter(otp = otp_code, email = email_adr)
                if otp_obj.exists():
                    # otp code provided is correct so verify it
                    a = otp_obj.first()
                    a.verified = True
                    a.save()

                    return Response({'status':True, 'detail':'OTP sucesfully verified', 'user':account['user']})
                else:
                    return Response({'status':False, 'detail':'Invalid OTP.'})
            else:
                return Response({'status':False, 'detail':'Phone number or email provided is invalid.'})
        else:
            return Response({'status':False, 'detail':account_exists['detail']})
    else:
        return Response({'otp':'This field is required.', 'email_or_phone':'This field is required.'})

@api_view(['POST'])
def reset_user_password(request):
    u_name = ''
    new_password_one = ''
    new_password_two = ''
    otp_code = ''
    try:
        u_name = str(request.data['username'])
        new_password_one = str(request.data['new_password1'])
        new_password_two = str(request.data['new_password2'])
        otp_code = str(request.data['otp'])
    except:
        pass

    if new_password_one and new_password_two and u_name and otp_code:
        user = ''
        try:
            user = User.objects.get(username = u_name)
        except:
            pass
        if user:
            # check if an otp object instance exists in the db
            otp = models.ResetPasswordOTP.objects.filter(Q(otp = otp_code, phone = user.phone) | Q(otp = otp_code, email = user.email))
            if otp.exists():
                if otp.first().verified == True:
                    if new_password_one == new_password_two:
                        user.set_password(new_password_one)
                        user.save()

                        # Since OTP has been verified and used to reset password, delete it to prevent reuse
                        otp.first().delete()
                        return Response({'status':True,'detail':'Password sucesfully changed. You can now use your new password to login to your account.'})
                    else:
                        return Response({'status':False,'detail':'new_password1 and new_password2 do not match!'})
                else:
                    return Response({'status':False,'detail':'OTP not verified. Verify OTP to confirm you own this account!'})
            else:
                return Response({'status':False,'detail':'Invalid OTP! Provide a valid OTP or request a new one.'})
        else:
            return Response({'statua':False,'detail':f'User {u_name} not found. Check username and try again!'})
    else:
        return Response({'new_password1':'This field is required.','new_password2':'This field is required.', 'username':'This field is required.', 'otp': 'This field is required.'})


"""
Reset password with OTP code views end here
"""

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

class ProfessionalGroupEditApi(RetrieveUpdateAPIView):
    queryset = models.ProfessionalGroup.objects.all()
    serializer_class = serializers.ProfessionalGroupSerializer
    permission_classes = [IsAuthenticated]

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
    filter_backends = [filters.OrderingFilter]
    ordering_fields  = ['likes','recommendation_rating','review_date']

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

# Filter food items based on their title/name
class PortfolioFilter(django_filters.FilterSet):
    town_name = django_filters.rest_framework.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = models.PortfolioItem
        fields = {
            'name'
        }

class PortfolioItemListApi(ListAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PortfolioFilter

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

# Service search history

class ServiceSearchHistoryListApi(ListAPIView):
    queryset = models.ServiceSearchHistory.objects.all()
    serializer_class = serializers.ServiceSearchHistorySerializer

class ServiceSearchHistoryDetailApi(RetrieveAPIView):
    queryset = models.ServiceSearchHistory.objects.all()
    serializer_class = serializers.ServiceSearchHistorySerializer

"""
 A custom api view for handling all the logic of creating
 and updating a search history object
"""
@api_view(['POST'])
def create_or_update_search_history(request):
    user_id = ''
    service_id = ''
    project_location_id = ''
    try:
        user_id = str(request.data['user_id'])
        service_id = str(request.data['service_id'])
        project_location_id = str(request.data['project_location_id'])
    except:
        pass

    if user_id and service_id and project_location_id:
        search_obj = models.ServiceSearchHistory.objects.filter(user = user_id, professional_service = service_id, project_location= project_location_id)
        response_message = ''
        if search_obj.exists():
            # don't create a new object, update the count only
            instance = search_obj.first()
            innitial_count = instance.search_count
            instance.search_count = innitial_count + 1
            instance.save()

            n_search = get_object_or_404(models.ServiceSearchHistory, pk=search_obj.first().pk)

            a = {
                "pk":n_search.pk,
                "user":n_search.user.username,
                "professional_service":n_search.professional_service.service_name,
                "project_location":n_search.project_location.town_name,
                "search_count":n_search.search_count,
                "search_date":n_search.search_date,
            }
            response_message = {'status':True, 'search':a }
        else:
            # create a search object
            user_obj = ''
            service_obj = ''
            project_location_obj = ''
            try:
                user_obj = User.objects.get(pk=user_id)
                service_obj = models.ProfessionalService.objects.get(pk=service_id)
                project_location_obj = location_models.KenyaTown.objects.get(pk=project_location_id)
            except:
                pass

            if user_obj and service_obj and project_location_obj:
                n_search = models.ServiceSearchHistory.objects.create(
                    user = user_obj,
                    professional_service = service_obj,
                    project_location = project_location_obj,
                    search_count = 1
                    )


                a = {
                    "pk":n_search.pk,
                    "user":n_search.user.username,
                    "professional_service":n_search.professional_service.service_name,
                    "project_location":n_search.project_location.town_name,
                    "search_count":n_search.search_count,
                    "search_date":n_search.search_date,
                }
                response_message = {'status':True, 'search':a }
            else:
                response_message = {'status':False, 'detail':f'User with user_id:{user_id} or Service with service_id:{service_id} do not exist or are invalid.'}

        return Response(response_message)

    else:
        return Response({'user_id':'This field is required.', 'service_id':'This field is required.','project_location_id':'This field is required.'})

def get_total_searches(service):
    """" Sort get key function for search_history_stats api view"""
    return service.get('total_searches')

def get_popular_searches(services, searches):
    services_array = []
    if services:
        for svc in services:
            search_items = searches.filter(professional_service=svc)
            if search_items.exists():
                total_search_count = 0
                for sch in search_items:
                    in_count = total_search_count
                    total_search_count = in_count + sch.search_count

                service_image_url = search_items.first().professional_service.service_image.url if search_items.first().professional_service.service_image else ''
                pro_group_image_url = search_items.first().professional_service.professional_category.professional_group.group_image.url if search_items.first().professional_service.professional_category.professional_group.group_image else ''

                if search_items.first().user:
                    service_obj = {
                        'user':search_items.first().user.username,
                        'professional_service':{
                                'pk':search_items.first().professional_service.pk,
                                'service_name':search_items.first().professional_service.service_name,
                                'service_image': service_image_url,
                                'slug':search_items.first().professional_service.slug,
                            },
                        'professional_group':{
                                "pk":search_items.first().professional_service.professional_category.professional_group.pk,
                                "group_name":search_items.first().professional_service.professional_category.professional_group.group_name,
                                "group_image":pro_group_image_url,
                                "slug":search_items.first().professional_service.professional_category.professional_group.slug,
                            },
                        'unique_search_count':search_items.count(),
                        'global_search_count':total_search_count,
                        'total_searches':search_items.count() + total_search_count
                    }

                    services_array.append(service_obj)
    popular_searcvices = sorted(services_array, key=get_total_searches, reverse=True)[0:10]
    return popular_searcvices

def get_recent_searches(services, searches):
    recent_searches_items = searches.order_by('-search_date')[0:10]
    recent_searches = []
    if recent_searches_items:
        for svc in recent_searches_items:
            service_image_url = svc.professional_service.service_image.url if svc.professional_service.service_image else ''
            if svc.user:
                service_obj = {
                    'user':svc.user.username,
                    'professional_service':{
                            'pk':svc.professional_service.pk,
                            'service_name':svc.professional_service.service_name,
                            'service_image': service_image_url,
                            'slug':svc.professional_service.slug,
                        },
                    'search_count':svc.search_count,
                    'search_date':svc.search_date,
                }

                recent_searches.append(service_obj)
    return recent_searches

@api_view(['GET'])
def search_history_stats(request):
    """
    Function will return statistic results for all searches made
    """
    searches = models.ServiceSearchHistory.objects.all()
    services = models.ProfessionalService.objects.all()
    # getting recent searches
    recent_searches = get_recent_searches(services,searches)
    # Get popular searches
    popular_searches = get_popular_searches(services,searches)
    return Response({'recent_searches':recent_searches,'popular_searches':popular_searches})

class MatchMakerListApi(ListAPIView):
    queryset = models.MatchMaker.objects.all()
    serializer_class = serializers.MatchMakerSerializer

class MatchMakerRetrieveApi(RetrieveAPIView):
    lookup_field = "professional_service"
    queryset = models.MatchMaker.objects.all()
    serializer_class = serializers.MatchMakerSerializer


import json
@api_view(['POST'])
def match_client_with_pros(request):
    questions = ""
    user_id = ""
    project_location_id = ""
    matchmaking_method = ""
    food_name = ""
    if request.user.is_authenticated:
        try:
            # We wil use this to define how we match the client and service provider
            # plus how to structure the results returned
            matchmaking_method = str(request.data['matchmaking_method'])
        except:
            pass
        
        try:
            # General fields common to all types of mathmaking methods
            user_id = str(request.data['user_id'])
            project_location_id = str(request.data['project_location_id'])
        except:
            pass
        
        if user_id and project_location_id:
            if matchmaking_method == "professionals":
                # special field(s) reuired for finding and returning professionals
                # in this matchmaking method
                try:
                    questions = request.data['questions']
                except:
                    pass
                
                # Find professionals
                if questions:
                    user_obj = ""
                    location_obj = ""
                    questions_valid = False
                    try:
                        user_obj = User.objects.get(pk=user_id)
                        location_obj = location_models.KenyaTown.objects.get(pk=project_location_id)
                        for q in questions:
                            question_obj = models.Question.objects.get(pk=q['question_id'])
                            for ans in q['answer']:
                                option_obj = models.QuestionOptions.objects.get(pk=ans)
                        questions_valid = True
                    except:
                        pass

                    if user_obj and location_obj and questions_valid== True:
                        pro_answers = models.ProAnswer.objects.all()

                        # TO DO: Check whether the answers provided are related to the questions

                        for q in questions:
                            # save the clients answer for each 1uestion
                            question_obj = models.Question.objects.get(pk=q['question_id'])
                            option_ids_list = q['answer']

                            client_answer_instance = models.ClientAnswer.objects.create(
                                            user = user_obj,
                                            question = question_obj,
                                            project_location = location_obj
                                        )

                            for a in option_ids_list:
                                option_obj = models.QuestionOptions.objects.get(pk=a)
                                client_answer_instance.answer.add(option_obj)

                            # Then Find pro answers that match the clients answer for the same question
                            pro_answers = models.ProAnswer.objects.filter(
                                            question = question_obj,
                                            service_delivery_areas__town_name__icontains = location_obj.town_name,
                                            answer__in = option_ids_list
                                            ).annotate(num_answer=Count('answer')).filter(num_answer=len(option_ids_list))

                        # After filtering the answers above create a list of business profile ids
                        # that we will use to filter the business profiel table for serializing
                        pro_ids =[]
                        for p in pro_answers:
                            pro_ids.append(p.business_profile.pk)

                        # Filter the business profile table
                        pros = models.BusinessProfile.objects.filter(pk__in=pro_ids)

                        # Serialize the data returned
                        serializer = serializers.BusinessProfileSerializer(pros,many=True)

                        return Response(serializer.data)
                    else:
                        return Response({'status':False, 'detail':'Not found. Provide valid values for required fields.'})
                else:
                    return Response({'questions':'This field is required',})
            elif matchmaking_method == "food":
                # special field(s) for finding and returning professionals
                # in this matchmaking method
                try:
                    food_name = str(request.data['food_name'])
                except:
                    pass
                
                # Find restaurants and return their menus related to the searched
                # food item
                if food_name:
                    user_obj = ""
                    location_obj = ""
                    try:
                        user_obj = User.objects.get(pk=user_id)
                        location_obj = location_models.KenyaTown.objects.get(pk=project_location_id)
                    except:
                        pass

                    if user_obj and location_obj:
                        # Filter the business profile table
                        menu = models.PortfolioItem.objects.filter(name__icontains= food_name)
                        restaurants = models.BusinessProfile.objects.filter(user=menu.created_by)
                        # Serialize the data returned
                        serializer = serializers.BusinessProfileSerializer(restaurants,many=True)

                        return Response(serializer.data)
                    else:
                        return Response({'status':False, 'detail':'Not found. Provide valid values for required fields.'})
                else:
                    return Response({'food_name':'This field is required'})
            else:
                return Response({'matchmaking_method':'Provide a valid matchmaking method. Valid methods are:- food or professionals.'})
        else:
            return Response({'user_id':'This field is required','project_location_id':'This field is required'})

@api_view(['GET'])
def search_food_item(request):
    key = ""
    try:
        key = str(request.GET.get('food_name', ''))
    except:
        pass
    
    if key:
        results = []
        proj_obj = models.PortfolioItem.objects
        projects = proj_obj.filter(name__icontains= key)
        for p in projects:
            name = p.name
            if name not in results:
                similar_items = proj_obj.filter(name__icontains= name).aggregate(cost=Avg('project_cost'))
                project = {
                    "pk":p.pk,
                    "name":name,
                    "service_name": p.project_job_type.service_name,
                    "avatar": p.project_job_type.service_image.url if p.project_job_type.service_image else '',
                    "average_price": similar_items["cost"]
                }
                results.append(project)

        return Response({'results':results}, status=status.HTTP_200_OK)
        
    else:
         return Response({'status':False, 'food_name':"This field is required"}, status=status.HTTP_400_BAD_REQUEST)
