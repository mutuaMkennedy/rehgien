from django.urls import path, include,re_path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('referral/payouts/list/', views.ReferralPayoutsListApi.as_view(), name='referral_payouts'),
    path('referral/system/list/', views.ReferralSystemListApi.as_view(), name='referral_system'),
    path('referral/code/submit/', views.validate_referral_code, name='submit_referral_code'),
    path('referral/recruiter/create/', views.create_recruiter_profile, name='RecruiterCreateApi'),
    path('referral/recruiter/<int:pk>/update/', views.RecruiterUpdateApi.as_view(), name='RecruiterUpdateApi'),
]
