from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # Leads
    path('pro/leads/list/', views.LeadsListApi, name='LeadsListApi'),
    path('pro/leads/<int:pk>/send_quote/', views.AddQuoteApi.as_view(), name='AddQuoteApi'),

    # Targeting preferences
    path('pro/targeting_preferences/update/', views.update_targeting_preferences, name='update_targeting_preferences'),

    path('pro/reviews/email_request/', views.send_email_review_requests, name='send_email_review_requests'),

    # Portflio items / Projects
    path('pro/portfolio_item/list/', views.PortfolioItemListApi.as_view(), name='PortfolioItemListApi'),
    path('pro/portfolio_item/create/', views.PortfolioItemCreateApi.as_view(), name='PortfolioItemCreateApi'),
    path('pro/portfolio_item/<int:pk>/update/', views.PortfolioItemUpdateApi.as_view(), name='PortfolioItemUpdateApi'),
    path('pro/portfolio_item/<int:pk>/delete/', views.PortfolioItemDeleteApi.as_view(), name='PortfolioItemDeleteApi'),

    # Portflio items / Projects
    path('pro/portfolio_item/photos/create/', views.PortfolioItemPhotoCreateApi.as_view(), name='PortfolioItemPhotoCreateApi'),
    path('pro/portfolio_item/photos/<int:pk>/update/', views.PortfolioItemPhotoUpdateApi.as_view(), name='PortfolioItemPhotoUpdateApi'),
    path('pro/portfolio_item/photos/<int:pk>/delete/', views.PortfolioItemPhotoDeleteApi.as_view(), name='PortfolioItemPhotoDeleteApi'),
]
