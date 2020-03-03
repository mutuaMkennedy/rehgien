from django.urls import path
from django.conf.urls import url
from . import views



app_name = 'search'

urlpatterns = [
	path('homes_for_sale/', views.onsale_search, name='onsale_search'),
	path('homes_for_rent/', views.rentals_search, name='rental_search'),
]
