from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact_listing_agent/', views.contact_listing_agent, name='contact_listing_agent'),
    path('contact_professional/', views.contact_pro, name='contact_pro'),
    path('about_rehgien/', views.about_us, name='about_us'),
    path('share_home/', views.share_listing, name='share_listing'),
    path('report/problem/pg', views.page_report, name = 'page_report'),
    path('report/problem/p_p', views.p_p_report, name = 'p_p_report'),
    path('report/problem/rv', views.review_report, name = 'review_report'),
]
