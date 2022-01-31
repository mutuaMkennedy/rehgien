from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
import json
from . import utils
from . import forms
from formtools.wizard.views import SessionWizardView
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError

# referencing the custom user model
User = get_user_model()

"""
Custom login view that allows login with phone or email
"""
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            identity = request.POST.get('identity','')
            password = request.POST.get('password','')
            if utils.is_email(identity):
                user_account = User.objects.filter(email=identity)
                if user_account:
                    user = authenticate(request, username=user_account.first().username, password=password)
                    if user is not None:
                        if user.user_type =='PRO':
                            login(request, user)
                            messages.success(request, 'Login successful!')
                            return redirect('rehgien_pro:dashboard_home')
                        else:
                            context = {
                            "identity":identity,
                            "password":password,
                            "permission_denied":'Only pros or service providers can login here. To login, use our mobile app instead.'
                            }
                            return render(request, 'app_accounts/login.html',context)
                    else:
                        context = {
                        "identity":identity,
                        "password":password,
                        "incorrect_password":'The password your entered is incorrect.'
                        }
                        return render(request, 'app_accounts/login.html',context)

                else:
                    context = {
                    "identity":identity,
                    "password":password,
                    "account_not_found":'The email you entered is not connected to an account.'
                    }
                    return render(request, 'app_accounts/login.html',context)

            elif utils.is_phone(identity):
                #  Format the phone number to include country code
                identity = '+254' + identity[-9:]
                user_account = User.objects.filter(phone=identity)
                if user_account:
                    user = authenticate(request, username=user_account.first().username, password=password)
                    if user is not None:
                        if user.user_type =='PRO':
                            login(request, user)
                            messages.success(request, 'Login successful!')
                            return redirect('rehgien_pro:dashboard_home')
                        else:
                            context = {
                            "identity":identity,
                            "password":password,
                            "permission_denied":'Only pros or service providers can login here. To login, use our mobile app instead.'
                            }
                            return render(request, 'app_accounts/login.html',context)
                    else:
                        context = {
                        "identity":identity,
                        "password":password,
                        "incorrect_password":'The password your entered is incorrect.'
                        }
                        return render(request, 'app_accounts/login.html',context)

                else:
                    context = {
                    "identity":identity,
                    "password":password,
                    "account_not_found":'The phone number you entered is not connected to an account.'
                    }
                    return render(request, 'app_accounts/login.html',context)
            else:
                context = {
                "identity":identity,
                "password":password,
                "invalid_identity":'Enter a valid email (E.g. xxx@domain.com ) or phone number (E.g. 07xxxxxxxx)'
                }
                return render(request, 'app_accounts/login.html',context)
        else:
            context={}
            return render(request, 'app_accounts/login.html',context)
    else:
        if request.user.user_type == 'PRO':
            return redirect('rehgien_pro:dashboard_home')
        else:
            return redirect('homepage')

def user_signup(request):
    context={}
    return render(request, 'app_accounts/sign_up.html',context)

"""
Custom sign up wizard to handle the various sign up steps
"""

def validate_phone_send_otp(request):
    phone = request.POST.get('phone',None)
    if phone:
        response = utils.validate_phone_send_otp(phone)
        if response['status'] == False:
            return JsonResponse(response)
        else:
            return JsonResponse(response)
    else:
        return JsonResponse({'status':False, 'detail':'Please enter a phone number!'})

#pro onboarding wizard
FORMS = [
            ("UserPhoneNumber", forms.UserPhoneNumber),
            # ("UserEmail", forms.UserEmail),
            ("PhoneVerificationCode", forms.PhoneVerificationCode),
            ("Password", forms.Password),
        ]

TEMPLATES = {
            "UserPhoneNumber": "app_accounts/sign_up/phone_number.html",
            # "UserEmail": "app_accounts/sign_up/email.html",
            "PhoneVerificationCode": "app_accounts/sign_up/phone_verification.html",
            "Password": "app_accounts/sign_up/password.html"
            }

# def show_message_form_condition(wizard):
#     # try to get the cleaned data of step 0
#     cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
#
#     # check if the field ``P`` was checked.
#
#     return cleaned_data.get('leave_message', True)


class UserAccountSetupWizardView(SessionWizardView):
    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        if request.user.is_authenticated:
            messages.error(request,'You are already signed in.')
            return HttpResponseRedirect('homepage')
        else:
            return super(UserAccountSetupWizardView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    # this runs for the step it's on as well as for the step before
    def get_form_initial(self, step):
        current_step = self.storage.current_step
        if step == 'PhoneVerificationCode':
            user_phone_number = self.storage.get_step_data('UserPhoneNumber').get('phone','')

            innitial = {
            'phone':user_phone_number,
            }
            return self.initial_dict.get(step, innitial)

        return self.initial_dict.get(step, {})


    def done(self, form_list, form_dict, **kwargs):
        # ProBusinessProfileImage = form_dict['ProBusinessProfileImage']
        # form_data = self.get_all_cleaned_data()
        # professional_services = form_data.pop('professional_services')
        # service_areas = form_data.pop('service_areas')
        # business_profile_image = form_data.pop('business_profile_image')
        #
        # obj_instance = profiles_models.BusinessProfile.objects.create(
        # **form_data, business_profile_image = resized_image,
        # user=self.request.user,
        # )

        context ={

        }
        return render(self.request, 'rehgien_pro/pro_onboarding/done.html',context)
