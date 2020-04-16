from django.urls import path, include
from django.conf.urls import url
from profiles.apis.views import (UserProfileView,
                                ProfileUpdateApi,
                                ProfileListApi,
                                ProfileDetailApi,
                                UserListingsListApi,
                                UsersListAPI,
                                UserAccountEditApi
                                    )

urlpatterns = [
    path('user/account/list/', UsersListAPI.as_view(), name='user_list' ),
    path('user/account/<int:pk>/edit/', UserAccountEditApi.as_view(), name='edit_account'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('profiles/list/', ProfileListApi.as_view(), name='user_profiles'),
    path('user/profile/<int:pk>/detail/', ProfileDetailApi.as_view(), name='profile_detail'),
    path('user/profile/<int:pk>/edit/', ProfileUpdateApi.as_view(), name='edit_profile'),
    path('user/listings/', UserListingsListApi.as_view(), name='listings_list'),
]
