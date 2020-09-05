from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'markets'

urlpatterns = [
    path('requests_list/', views.request_list, name = 'request_list'),
    path('property_request/create', views.property_request_lead, name = 'property_request'),
    path('proffesional_request/create', views.proffesional_request_lead, name = 'proffesional_request'),
    path('other_request/create', views.other_request_lead, name = 'other_request'),
    path('agent_lead_request/create', views.agent_lead_request, name = 'agent_lead_request'),
    path('agent_property_request/create', views.agent_property_request, name = 'agent_property_request'),
    # update views
    path('property_request/<int:pk>/update', views.property_request_lead_update, name = 'property_request_update'),
    path('proffesional_request/<int:pk>/update', views.proffesional_request_lead_update, name = 'pro_request_update'),
    path('other_request/<int:pk>/update', views.other_request_lead_update, name = 'other_request_update'),
    path('agent_lead_request/<int:pk>/update', views.agent_lead_request_update, name = 'agent_lead_request_update'),
    path('agent_property_request/<int:pk>/update', views.agent_property_request_update, name = 'agent_prop_request_update'),
    #Deactivate views
    path('property_request/<int:pk>/deactivate', views.property_request_lead_deactivate, name = 'property_request_deactivate'),
    path('proffesional_request/<int:pk>/deactivate', views.proffesional_request_lead_deactivate, name = 'pro_request_deactivate'),
    path('other_request/<int:pk>/deactivate', views.other_request_lead_deactivate, name = 'other_request_deactivate'),
    path('agent_lead_request/<int:pk>/deactivate', views.agent_lead_request_deactivate, name = 'agent_lead_request_deactivate'),
    path('agent_property_request/<int:pk>/deactivate', views.agent_property_request_deactivate, name = 'agent_prop_request_deactivate')
]
