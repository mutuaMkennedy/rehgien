from django.urls import path, include
from django.conf.urls import url
from profiles.apis.views import UserProfileView,ProfileUpdateApi

urlpatterns = [
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/<int:pk>/edit/', ProfileUpdateApi.as_view(), name='edit_profile'),
]
