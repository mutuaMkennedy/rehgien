from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    path('email/', views.send_email, name='send_email'),
    path('about_us/', views.about_us, name="about_us"),
]
