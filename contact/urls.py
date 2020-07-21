from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    path('email/', views.send_message, name='send_message'),
    path('about_us/', views.about_us, name="about_us"),
]
