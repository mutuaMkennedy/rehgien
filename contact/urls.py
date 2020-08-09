from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact_listing_agent/', views.contact_listing_agent, name='contact_listing_agent'),
    path('contact_professional/', views.contact_pro, name='contact_pro'),
    path('about_rehgien/', views.about_us, name='about_us'),
    path('share_home/', views.share_listing, name='share_listing'),
]
