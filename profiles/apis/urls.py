from django.urls import path, include
from django.conf.urls import url
from profiles.apis import views as api_views
from . import views

urlpatterns = [
    path('user/account/list/', api_views.UsersListAPI.as_view(), name='user_list' ),
    path('user/account/<int:pk>/edit/', api_views.UserAccountEditApi.as_view(), name='edit_account'),
    path('user/listings/property/homes/', api_views.UserListingsListApi.as_view(), name='listings_list'),
    path('profiles/professional_group/list/', api_views.ProfessionalGroupListApi.as_view(), name='ProfessionalGroupListApi'),
    path('profiles/professional_category/list/', api_views.ProfessionalCategoryListApi.as_view(), name='ProfessionalCategoryListApi'),
    path('profiles/professional_service/list/', api_views.ProfessionalServiceListApi.as_view(), name='ProfessionalServiceListApi'),
    path('profiles/business_profile/list/', api_views.BusinessProfileListApi.as_view(), name='business_profile_list'),
    path('profiles/business_profile/<int:pk>/retrieve/', api_views.BusinessProfileDetailApi.as_view(), name='business_profile_retrieve'),
    path('profiles/business_profile/<int:pk>/edit/', api_views.BusinessProfileUpdateApi.as_view(), name='business_profile_update'),

    path('profiles/business_review/list/', api_views.ReviewListApi.as_view(), name='business_review_list'),
    path('profiles/business_review/create/', api_views.ReviewCreateApi.as_view(), name='business_review_create'),

    path('profiles/portfolio_item/create/', api_views.PortfolioItemCreateApi.as_view(), name='portfolio_item_create'),
    path('profiles/portfolio_item/list/', api_views.PortfolioItemListApi.as_view(), name='portfolio_item_list'),
    path('profiles/portfolio_item/<int:pk>/retrieve/', api_views.PortfolioItemDetailApi.as_view(), name='portfolio_item_retrieve'),
    path('profiles/portfolio_item/<int:pk>/update/', api_views.PortfolioItemUpdateApi.as_view(), name='portfolio_item_update'),
    path('profiles/portfolio_item/<int:pk>/delete/', api_views.PortfolioItemDeleteApi.as_view(), name='portfolio_item_delete'),

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
    ]
