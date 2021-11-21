from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import json
from . import utils

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
