from django.urls import path, include,re_path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('referral/payouts/list/', views.ReferralPayoutsListApi.as_view(), name='referral_payouts'),
    path('referral/system/list/', views.ReferralSystemListApi.as_view(), name='referral_system'),
    path('referral/code/submit/', views.validate_referral_code, name='submit_referral_code'),
]
