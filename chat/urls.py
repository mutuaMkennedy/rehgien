from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'chat'

urlpatterns = [
    path('twilio/get_token/', views.get_twilio_acess_token, name='get_twilio_acess_token'),
    path('twilio/delete/conversation/', views.deleteConversation, name = 'deleteConversation'),
]
