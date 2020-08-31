from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'markets'

urlpatterns = [
    path('property_request/create', views.property_request_lead, name = 'property_request'),
    path('proffesional_request/create', views.proffesional_request_lead, name = 'proffesional_request'),
    path('other_request/create', views.other_request_lead, name = 'other_request')
]
