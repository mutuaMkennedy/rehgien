from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'chat'

urlpatterns = [
    url(r'user_token/$', views.user_token, name="user_token"),
    path('pro_rooms/', views.chat_room, name='chat_room'),
]
