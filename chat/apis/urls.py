from django.urls import path, include,re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('chat/twilio/access_token/', views.get_twilio_access_token, name = 'get_twilio_access_token'),
]
