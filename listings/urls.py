from django.urls import path,include
from django.conf.urls import url
from . import views

app_name = 'listings'

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	path('buy/', views.sale_listings_results, name='sale_listings'),
	path('rent/', views.rental_listings_results, name='rental_listings'),
	url(r'^onsale/(?P<pk>[0-9]+)/$', views.onsale_detail, name='onsale_detail'),
	path('on_sale/favourite/<int:pk>/', views.onsale_favourite, name='s_favourite'),
	path('on_sale/ajx_favourite/', views.ajxonsale_favourite, name='axs_favourite'),
	path('for_rent/ajx_favourite/', views.ajxrental_favourite, name='axr_favourite'),
	url(r'^rental/(?P<pk>[0-9]+)/$', views.rental_detail, name='rental_detail'),
	path('rental/favourite/<int:pk>/', views.rental_favourite, name='r_favourite'),
	path('on_sale/<int:pk>/edit/', views.for_sale_update, name='update'),
	path('rental/<int:pk>/edit/', views.for_rent_update, name='rental_update'),
	path('on_sale/<int:pk>/delete/', views.for_sale_delete, name='s_delete'),
	path('rental/<int:pk>/delete/', views.for_rent_delete, name='r_delete'),
	url(r'sell/$', views.listing_form, name='sell_listing_form'),
	url(r'list_your_rental/$', views.rental_listing_form, name='rental_listing_form'),
	url(r'^sale_like/$', views.sale_like, name = 'sale_like'),
	# url(r'^directions/$', views.directions, name = 'directions'),
	#url(r'^search/autocomplete/$', views.autocomplete),
    #url(r'^find/', views.FacetedSearchView.as_view(), name='haystack_search'),
	#rl(r'^find/rentals', views.rental_results, name='rental_search'),
	#APis

]
