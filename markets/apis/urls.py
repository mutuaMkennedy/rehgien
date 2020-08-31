from django.urls import path
from django.conf.urls import url
from markets.apis.views import (
        PropertyRequestLeadApi, PropertyRequestLeadCreateApi, PropertyRequestLeadDetailApi,
        PropertyRequestLeadUpdateApi, PropertyRequestLeadDeleteApi, ProffesionalRequestLeadApi,
        ProffesionalRequestLeadCreateApi, ProffesionalRequestLeadDetailApi, ProffesionalRequestLeadUpdateApi,
        ProffesionalRequestLeadDeleteApi, OtherServiceLeadApi, OtherServiceLeadCreateApi,
        OtherServiceLeadDetailApi, OtherServiceLeadUpdateApi, OtherServiceLeadDeleteApi,
        AgentLeadRequestApi, AgentLeadRequestCreateApi, AgentLeadRequestDetailApi,
        AgentLeadRequestUpdateApi, AgentLeadRequestDeleteApi, AgentPropertyRequestApi,
        AgentPropertyRequestCreateApi, AgentPropertyRequestDetailApi,
        AgentPropertyRequestUpdateApi, AgentPropertyRequestDeleteApi, ClaimReferPropertyRequestLeadApi,
        ClaimReferProRequestLeadApi,ClaimReferOtherServiceLeadApi,ClaimReferAgentLeadRequestApi,
        ClaimReferAgentPropertyRequestApi

        )

urlpatterns = [
    #PropertyRequestLeadApi
    path('markets/request_property/', PropertyRequestLeadApi.as_view(), name='rq_property_list_api'),
    path('markets/request_property/create/', PropertyRequestLeadCreateApi.as_view(), name='rq_property_create_api'),
    url(r'^markets/request_property/(?P<pk>[0-9]+)/$', PropertyRequestLeadDetailApi.as_view(), name='rq_property_detail_api'),
    path('markets/request_property/<int:pk>/edit/', PropertyRequestLeadUpdateApi.as_view(), name='rq_property_update_api'),
    path('markets/request_property/<int:pk>/cl_or_re/', ClaimReferPropertyRequestLeadApi.as_view(), name='c_r_rq_property_api'),
    path('markets/request_property/<int:pk>/delete/', PropertyRequestLeadDeleteApi.as_view(), name='rq_property_api'),
    # ProffesionalRequestLead
    path('markets/pro_request/', ProffesionalRequestLeadApi.as_view(), name='pro_request_list_api'),
    path('markets/pro_request/create/', ProffesionalRequestLeadCreateApi.as_view(), name='pro_request_create_api'),
    url(r'^markets/pro_request/(?P<pk>[0-9]+)/$', ProffesionalRequestLeadDetailApi.as_view(), name='pro_request_detail_api'),
    path('markets/pro_request/<int:pk>/edit/', ProffesionalRequestLeadUpdateApi.as_view(), name='pro_request_update_api'),
    path('markets/pro_request/<int:pk>/cl_or_re/', ClaimReferProRequestLeadApi.as_view(), name='c_r_pro_request_api'),
    path('markets/pro_request/<int:pk>/delete/', ProffesionalRequestLeadDeleteApi.as_view(), name='pro_request_delete_api'),
    # OtherRequestLead
    path('markets/other_service_request/', OtherServiceLeadApi.as_view(), name='os_request_list_api'),
    path('markets/other_service_request/create/', OtherServiceLeadCreateApi.as_view(), name='os_request_create_api'),
    url(r'^markets/other_service_request/(?P<pk>[0-9]+)/$', OtherServiceLeadDetailApi.as_view(), name='os_request_detail_api'),
    path('markets/other_service_request/<int:pk>/edit/', OtherServiceLeadUpdateApi.as_view(), name='os_request_update_api'),
    path('markets/other_service_request/<int:pk>/cl_or_re/', ClaimReferOtherServiceLeadApi.as_view(), name='c_r_os_request_api'),
    path('markets/other_service_request/<int:pk>/delete/', OtherServiceLeadDeleteApi.as_view(), name='os_request_delete_api'),
    # AgentLeadRequest
    path('markets/agent_lead_request/', AgentLeadRequestApi.as_view(), name='ag_lead_request_list_api'),
    path('markets/agent_lead_request/create/', AgentLeadRequestCreateApi.as_view(), name='ag_lead_request_create_api'),
    url(r'^markets/agent_lead_request/(?P<pk>[0-9]+)/$', AgentLeadRequestDetailApi.as_view(), name='ag_lead_request_detail_api'),
    path('markets/agent_lead_request/<int:pk>/edit/', AgentLeadRequestUpdateApi.as_view(), name='ag_lead_request_update_api'),
    path('markets/agent_lead_request/<int:pk>/cl_or_re/', ClaimReferAgentLeadRequestApi.as_view(), name='c_r_ag_lead_request_api'),
    path('markets/agent_lead_request/<int:pk>/delete/', AgentLeadRequestDeleteApi.as_view(), name='ag_lead_request_delete_api'),
    # AgentPropertyRequest
    path('markets/agent_property_request/', AgentPropertyRequestApi.as_view(), name='ag_prop_request_list_api'),
    path('markets/agent_property_request/create/', AgentPropertyRequestCreateApi.as_view(), name='ag_prop_request_create_api'),
    url(r'^markets/agent_property_request/(?P<pk>[0-9]+)/$', AgentPropertyRequestDetailApi.as_view(), name='ag_prop_request_detail_api'),
    path('markets/agent_property_request/<int:pk>/edit/', AgentPropertyRequestUpdateApi.as_view(), name='ag_prop_request_update_api'),
    path('markets/agent_property_request/<int:pk>/cl_or_re/', ClaimReferAgentPropertyRequestApi.as_view(), name='c_r_ag_prop_request_api'),
    path('markets/agent_property_request/<int:pk>/delete/', AgentPropertyRequestDeleteApi.as_view(), name='ag_prop_request_delete_api'),
]
