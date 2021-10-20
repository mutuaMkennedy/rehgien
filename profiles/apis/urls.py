from django.urls import path, include,re_path
from django.conf.urls import url
from profiles.apis import views as api_views
from . import views
from . import social_authentication

urlpatterns = [
    # Custom api endpoint for checking is user exists in login
    re_path(r'^user/account/lookup/$', api_views.lookup_user_obj_for_login, name = 'lookup_email_or_phone'),
    path('user/account/list/', api_views.UsersListAPI.as_view(), name='user_list' ),
    path('user/account/<int:pk>/retrieve/', api_views.UsersAccountRetrieve.as_view(), name='UsersAccountRetrieve' ),
    path('user/account/<int:pk>/edit/', api_views.UserAccountEditApi.as_view(), name='edit_account'),
    path('user/listings/property/homes/', api_views.UserListingsListApi.as_view(), name='listings_list'),
    path('profiles/professional_group/list/', api_views.ProfessionalGroupListApi.as_view(), name='ProfessionalGroupListApi'),
    path('profiles/professional_group/<int:pk>/edit/', api_views.ProfessionalGroupEditApi.as_view(), name='ProfessionalGroupEditApi'),
    path('profiles/professional_category/list/', api_views.ProfessionalCategoryListApi.as_view(), name='ProfessionalCategoryListApi'),
    path('profiles/professional_service/list/', api_views.ProfessionalServiceListApi.as_view(), name='ProfessionalServiceListApi'),
    path('profiles/business_profile/list/', api_views.BusinessProfileListApi.as_view(), name='business_profile_list'),
    path('profiles/business_profile/<int:pk>/retrieve/', api_views.BusinessProfileDetailApi.as_view(), name='business_profile_retrieve'),
    path('profiles/business_profile/<int:pk>/edit/', api_views.BusinessProfileUpdateApi.as_view(), name='business_profile_update'),
    path('profiles/business_profile/<int:pk>/social/', api_views.SocialBusinessProfileUpdateApi.as_view(), name='SocialBusinessProfileUpdateApi'),

    path('profiles/business_review/list/', api_views.ReviewListApi.as_view(), name='business_review_list'),
    path('profiles/business_review/create/', api_views.ReviewCreateApi.as_view(), name='business_review_create'),
    path('profiles/business_review/<int:pk>/like/', api_views.LikeReviewUpdateApi.as_view(), name='LikeReviewUpdateApi'),

    path('profiles/portfolio_item/create/', api_views.PortfolioItemCreateApi.as_view(), name='portfolio_item_create'),
    path('profiles/portfolio_item/list/', api_views.PortfolioItemListApi.as_view(), name='portfolio_item_list'),
    path('profiles/portfolio_item/<int:pk>/retrieve/', api_views.PortfolioItemDetailApi.as_view(), name='portfolio_item_retrieve'),
    path('profiles/portfolio_item/<int:pk>/update/', api_views.PortfolioItemUpdateApi.as_view(), name='portfolio_item_update'),
    path('profiles/portfolio_item/<int:pk>/delete/', api_views.PortfolioItemDeleteApi.as_view(), name='portfolio_item_delete'),

    path('profiles/portfolio_item/photo/create/', api_views.PortfolioItemPhotoCreateApi.as_view(), name='PortfolioItemPhotoCreateApi'),
    path('profiles/portfolio_item/photo/list/', api_views.PortfolioItemPhotoListApi.as_view(), name='PortfolioItemPhotoListApi'),
    path('profiles/portfolio_item/photo/<int:pk>/retrieve/', api_views.PortfolioItemPhotoDetailApi.as_view(), name='PortfolioItemPhotoDetailApi'),
    path('profiles/portfolio_item/photo/<int:pk>/update/', api_views.PortfolioItemPhotoUpdateApi.as_view(), name='PortfolioItemPhotoUpdateApi'),
    path('profiles/portfolio_item/photo/<int:pk>/delete/', api_views.PortfolioItemPhotoDeleteApi.as_view(), name='PortfolioItemPhotoDeleteApi'),

    path('profiles/team_connection/create/', api_views.TeammateConnectionCreate.as_view(), name='team_connection_create'),
    path('profiles/team_connection/list/', api_views.TeammateConnectionListApi.as_view(), name='team_connection_list'),
    path('profiles/team_connection/<int:pk>/retrieve/', api_views.TeammateConnectionDetailApi.as_view(), name='team_connection_retrieve'),
    path('profiles/team_connection/<int:pk>/update/', api_views.TeammateConnectionUpdateApi.as_view(), name='team_connection_update'),
    path('profiles/team_connection/<int:pk>/delete/', api_views.TeammateConnectionDeleteApi.as_view(), name='team_connection_delete'),

    path('profiles/business_hours/create/', api_views.BusinessHoursCreate.as_view(), name='business_hours_create'),
    path('profiles/business_hours/list/', api_views.BusinessHoursListApi.as_view(), name='business_hours_list'),
    path('profiles/business_hours/<int:pk>/retrieve/', api_views.BusinessHoursDetailApi.as_view(), name='business_hours_retrieve'),
    path('profiles/business_hours/<int:pk>/update/', api_views.BusinessHoursUpdateApi.as_view(), name='business_hours_update'),
    path('profiles/business_hours/<int:pk>/delete/', api_views.BusinessHoursDeleteApi.as_view(), name='business_hours_delete'),

    path('profiles/client/create/', api_views.ClientCreate.as_view(), name='client_create'),
    path('profiles/client/list/', api_views.ClientListApi.as_view(), name='client_list'),
    path('profiles/client/<int:pk>/retrieve/', api_views.ClientDetailApi.as_view(), name='client_retrieve'),
    path('profiles/client/<int:pk>/update/', api_views.ClientUpdateApi.as_view(), name='client_update'),
    path('profiles/client/<int:pk>/delete/', api_views.ClientDeleteApi.as_view(), name='client_delete'),

    #OTP send and verification URLs
    path('otp/verify_phone/send_otp/', api_views.validate_phone_send_otp, name = 'send_otp'),
    path('otp/verify_phone/verify_otp/', api_views.validate_sent_otp, name = 'verify_sent_otp'),

    # social authentication url endpoints
    path('rest-auth/facebook/', social_authentication.FacebookLogin.as_view(), name = 'fb_login'),
    path('rest-auth/google/', social_authentication.GoogleLogin.as_view(), name = 'google_login'),

    # Password reset with OTP
    path('account/password/reset/send_otp/', api_views.send_otp_to_email_or_phone, name = 'send_password_reset_otp'),
    path('account/password/reset/verify_otp/', api_views.verify_password_reset_otp, name = 'verify_password_reset_otp'),
    path('account/password/reset/confirm/', api_views.reset_user_password, name = 'reset_user_password'),

    # Search history
    path('search/search_history/list/', api_views.ServiceSearchHistoryListApi.as_view(), name = 'search_history'),
    path('search/search_history/<int:pk>/retrieve/', api_views.ServiceSearchHistoryDetailApi.as_view(), name = 'search_history_retrieve'),
    path('search/search_history/save/', api_views.create_or_update_search_history, name = 'create_or_update_search_history'),
    path('search/search_history/stats/', api_views.search_history_stats, name = 'search_history_stats'),

    # Matchmaking Process
    path('search/matchmaking/questions/list/', api_views.MatchMakerListApi.as_view(), name = 'match_maker_list'),
    path('search/matchmaking/questions/<int:professional_service>/retrieve/', api_views.MatchMakerRetrieveApi.as_view(), name = 'match_maker_retrieve'),
    path('search/matchmaking/pros/find_match/', api_views.match_client_with_pros, name = 'match_client_with_pros'),
    ]
