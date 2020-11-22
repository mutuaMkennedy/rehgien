from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'listings'

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	re_path(r'^(?P<property_category>\w+)/(?P<property_listing_type>\w+)/$', views.property_listings_results, name='property-listings'),
	re_path(r'^(?P<property_category>\w+)/property_id/(?P<pk>[0-9]+)/$', views.property_detail, name='property_detail'),
	re_path(r'^save_property/$', views.save_property, name='save_property'),
	re_path(r'^(?P<property_category>\w+)/(?P<pk>[0-9]+)/edit/', views.property_update, name='property_update'),
	re_path(r'^(?P<property_category>\w+)/(?P<pk>[0-9]+)/delete/$', views.property_delete, name='property_delete'),
	url(r'property/add/$', views.property_listing_form, name='property_listing_form'),
	# url(r'^directions/$', views.directions, name = 'directions'),
	#url(r'^search/autocomplete/$', views.autocomplete),
    #url(r'^find/', views.FacetedSearchView.as_view(), name='haystack_search'),
	#rl(r'^find/rentals', views.rental_results, name='rental_search'),

]
