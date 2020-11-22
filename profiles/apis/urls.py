from django.urls import path, include
from django.conf.urls import url
from profiles.apis.views import (
                                UserListingsListApi,
                                UsersListAPI,
                                UserAccountEditApi,
                                AgentProfileListApi,
                                AgentProfileDetailApi,
                                AgentProfileUpdateApi,
                                AgentReviewsListApi,
                                AgentReviewsCreateApi,
                                PropertyManagerProfileListApi,
                                PropertyManagerProfileDetailApi,
                                PropertyManagerProfileUpdateApi,
                                PropertyManagerReviewsListApi,
                                PropertyManagerReviewsCreateApi,
                                DesignAndServiceProProfileListApi,
                                DesignAndServiceProProfileDetailApi,
                                DesignAndServiceProProfileUpdateApi,
                                DesignAndServiceProReviewsListApi,
                                DesignAndServiceProReviewsCreateApi,
                                CompanyProfileListApi,
                                CompanyProfileDetailApi,
                                CompanyProfileUpdateApi,
                                CompanyReviewsListApi,
                                CompanyReviewsCreateApi,
                                DesignAndServiceProProjectsApi,
                                DesignAndServiceProProjectsListApi,
                                DesignAndServiceProProjectsDetailApi,
                                DesignAndServiceProProjectsUpdateApi,
                                DesignAndServiceProProjectsDeleteApi,
                                PMPortfolioCreateApi,
                                PMPortfolioListApi,
                                PMPortfolioDetailApi,
                                PMPortfolioUpdateApi,
                                PMPortfolioDeleteApi,
                                TeammateConnectionApi,
                                TeammateConnectionListApi,
                                TeammateConnectionDetailApi,
                                TeammateConnectionUpdateApi,
                                TeammateConnectionDeleteApi
                                    )
from . import views

urlpatterns = [
    path('user/account/list/', UsersListAPI.as_view(), name='user_list' ),
    path('user/account/<int:pk>/edit/', UserAccountEditApi.as_view(), name='edit_account'),
    path('user/listings/property/homes/', UserListingsListApi.as_view(), name='listings_list'),

    path('profiles/companies/', CompanyProfileListApi.as_view(), name='CompanyProfile'),
    path('profiles/companies/<int:pk>/detail/', CompanyProfileDetailApi.as_view(), name='CompanyProfile'),
    path('profiles/companies/<int:pk>/edit/', CompanyProfileUpdateApi.as_view(), name='CompanyProfile'),

    path('profiles/agents/', AgentProfileListApi.as_view(), name='agent_profiles'),
    path('profiles/agents/<int:pk>/detail/', AgentProfileDetailApi.as_view(), name='profile_detail'),
    path('profiles/agents/<int:pk>/edit/', AgentProfileUpdateApi.as_view(), name='agent_eProfile'),

    path('profiles/propertyManagers/', PropertyManagerProfileListApi.as_view(), name='pm_profiles'),
    path('profiles/propertyManagers/<int:pk>/detail/', PropertyManagerProfileDetailApi.as_view(), name='pm_detail'),
    path('profiles/propertyManagers/<int:pk>/edit/', PropertyManagerProfileUpdateApi.as_view(), name='pm_eProfile'),

    path('profiles/design&servicePros/', DesignAndServiceProProfileListApi.as_view(), name='ds_profiles'),
    path('profiles/design&servicePros/<int:pk>/detail/', DesignAndServiceProProfileDetailApi.as_view(), name='ds_detail'),
    path('profiles/design&servicePros/<int:pk>/edit/', DesignAndServiceProProfileUpdateApi.as_view(), name='ds_eProfile'),

    path('profiles/companyReviews/', CompanyReviewsListApi.as_view(), name='company_reviews'),
    path('profiles/companyReviews/create/', CompanyReviewsCreateApi.as_view(), name='company_rv_create'),

    path('profiles/agentReviews/', AgentReviewsListApi.as_view(), name='agent_reviews'),
    path('profiles/agentReviews/create/', AgentReviewsCreateApi.as_view(), name='agent_rv_create'),

    path('profiles/propertyManagerReviews/', PropertyManagerReviewsListApi.as_view(), name='pm_reviews'),
    path('profiles/propertyManagerReviews/create/', PropertyManagerReviewsCreateApi.as_view(), name='pm_rv_create'),

    path('profiles/design&serviceProsReviews/', DesignAndServiceProReviewsListApi.as_view(), name='ds_reviews'),
    path('profiles/design&serviceProsReviews/create/', DesignAndServiceProReviewsCreateApi.as_view(), name='ds_rv_create'),

    path('profiles/pmPortfolio/property/create/', PMPortfolioCreateApi.as_view(), name='pm_property_create'),
    path('profiles/pmPortfolio/properties/', PMPortfolioListApi.as_view(), name='pm_property'),
    path('profiles/pmPortfolio/property/<int:pk>/detail/', PMPortfolioDetailApi.as_view(), name='pm_property_detail'),
    path('profiles/pmPortfolio/property/<int:pk>/update/', PMPortfolioUpdateApi.as_view(), name='pm_property_update'),
    path('profiles/pmPortfolio/property/<int:pk>/delete/', PMPortfolioDeleteApi.as_view(), name='pm_property_delete'),

    path('profiles/design&servicePro/project/create/', DesignAndServiceProProjectsApi.as_view(), name='ds_project_create'),
    path('profiles/design&servicePro/projects/', DesignAndServiceProProjectsListApi.as_view(), name='ds_projects'),
    path('profiles/design&servicePro/project/<int:pk>/detail/', DesignAndServiceProProjectsDetailApi.as_view(), name='ds_detail'),
    path('profiles/design&servicePro/project/<int:pk>/update/', DesignAndServiceProProjectsUpdateApi.as_view(), name='ds_update'),
    path('profiles/design&servicePro/project/<int:pk>/delete/', DesignAndServiceProProjectsDeleteApi.as_view(), name='ds_delete'),

    path('profiles/teamConnection/create/', TeammateConnectionApi.as_view(), name='teamC_create'),
    path('profiles/teamConnection/list/', TeammateConnectionListApi.as_view(), name='teamC_list'),
    path('profiles/teamConnection/<int:pk>/detail', TeammateConnectionDetailApi.as_view(), name='teamC_detail'),
    path('profiles/teamConnection/<int:pk>/update/', TeammateConnectionUpdateApi.as_view(), name='teamC_update'),
    path('profiles/teamConnection/<int:pk>/delete/', TeammateConnectionDeleteApi.as_view(), name='teamC_delete'),

    ]
