from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('contact/messaging/message_property_listing_owner/', views.contact_listing_agent, name='contact_listing_agent' ),
    path('contact/messaging/message_professional/', views.contact_pro, name='contact_pro' ),
    path('share/property/home/send_email/', views.share_listing, name='share_listing' ),
    path('report_problem/report_business_page/', views.PageReportApi.as_view(), name='report_business_page' ),
    path('report_problem/report_portfolio_object/', views.PortfolioReportApi.as_view(), name='report_portfolio_object' ),
    path('report_problem/report_posted_review/', views.ReviewReportApi.as_view(), name='report_posted_review' ),
    ]
