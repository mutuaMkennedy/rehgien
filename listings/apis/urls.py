from django.urls import path, include
from django.conf.urls import url
from listings.apis.views import (
                ApartmentsForSaleListApi,MansionsForSaleListApi,
                BungalowsForSaleListApi,CondosForSaleListApi,
                DormsForSaleListApi,DuplexForSaleListApi,
                SingleFamilyForSaleListApi,TerracedForSaleListApi,
                TownHouseForSaleListApi,OthersForSaleListApi,
                ForSaleListApi,
                ForSaleCreateApi,
                ForSaleDetailApi,
                ForSaleUpdateApi,
                ForSaleDeleteApi,
                ApartmentsForRentListApi,MansionsForRentListApi,
                BungalowsForRentListApi,CondosForRentListApi,
                DormsForRentListApi,DuplexForRentListApi,
                SingleFamilyForRentListApi,TerracedForRentListApi,
                TownHouseForRentListApi,OthersForRentListApi,
                ForRentListApi,
                ForRentCreateApi,
                ForRentDetailApi,
                ForRentUpdateApi,
                ForRentDeleteApi
                )
# from rest_framework import routers
#
# router=routers.DefaultRouter()
# router.register('OnsaleListings', views.onSaleViewSet())

urlpatterns = [
    #normal for sale url endpoints
    path('homes-for-sale/', ForSaleListApi.as_view(), name='for_sale_list_api'),
    path('homes-for-sale/create/', ForSaleCreateApi.as_view(), name='onsale_create_api'),
    url(r'^homes-for-sale/(?P<pk>[0-9]+)/$', ForSaleDetailApi.as_view(), name='onsale_detail_api'),
    path('homes-for-sale/<int:pk>/edit/', ForSaleUpdateApi.as_view(), name='onsale_update_api'),
    path('homes-for-sale/<int:pk>/delete/', ForSaleDeleteApi.as_view(), name='onsale_delete_api'),
    #normal rental url endpoints
    path('homes-for-rent/', ForRentListApi.as_view(), name='rentals_list_api'),
    path('homes-for-rent/create/', ForRentCreateApi.as_view(), name='rentals_create_api'),
    url(r'^homes-for-rent/(?P<pk>[0-9]+)/$', ForRentDetailApi.as_view(), name='rentals_detail_api'),
    path('homes-for-rent/<int:pk>/edit/', ForRentUpdateApi.as_view(), name='rentals_update_api'),
    path('homes-for-rent/<int:pk>/delete/', ForRentDeleteApi.as_view(), name='rentals_delete_api'),
    #filtered for sale list url endpoints as per type/category
    path('apartments-for-sale/', ApartmentsForSaleListApi.as_view(), name='apartments_onsale_list_api'),
    path('mansions-for-sale/', MansionsForSaleListApi.as_view(), name='mansions_onsale_list_api'),
    path('bungalows-for-sale/', BungalowsForSaleListApi.as_view(), name='bungalows_onsale_list_api'),
    path('condos-for-sale/', CondosForSaleListApi.as_view(), name='condos_onsale_list_api'),
    path('dorms-for-sale/', DormsForSaleListApi.as_view(), name='dorms_onsale_list_api'),
    path('duplex-for-sale/', DuplexForSaleListApi.as_view(), name='duplex_onsale_list_api'),
    path('singlefamily-homes-for-sale/', SingleFamilyForSaleListApi.as_view(), name='singlefamily_onsale_list_api'),
    path('terraced-homes-for-sale/', TerracedForSaleListApi.as_view(), name='terraced_onsale_list_api'),
    path('townhouses-for-sale/', TownHouseForSaleListApi.as_view(), name='townhouse_onsale_list_api'),
    path('othertypes-for-sale/', OthersForSaleListApi.as_view(), name='othertypes_onsale_list_api'),
    #filtered rental list url endpoints as per type/category
    path('apartments-for-rent/', ApartmentsForRentListApi.as_view(), name='rental_apartments_list_api'),
    path('mansions-for-rent/', MansionsForRentListApi.as_view(), name='rental_mansions_list_api'),
    path('bungalows-for-rent/', BungalowsForRentListApi.as_view(), name='rental_bungalows_list_api'),
    path('condos-for-rent/', CondosForRentListApi.as_view(), name='rental_condos_list_api'),
    path('dorms-for-rent/', DormsForRentListApi.as_view(), name='rental_dorms_list_api'),
    path('duplex-for-rent/', DuplexForRentListApi.as_view(), name='rental_duplex_list_api'),
    path('singlefamily-homes-for-rent/', SingleFamilyForRentListApi.as_view(), name='rental_singlefamily_list_api'),
    path('terraced-homes-for-rent/', TerracedForRentListApi.as_view(), name='rental_terraced_list_api'),
    path('townhouses-for-rent/', TownHouseForRentListApi.as_view(), name='rental_townhouse_list_api'),
    path('othertypes-for-rent/', OthersForRentListApi.as_view(), name='rental_othertypes_list_api'),

]
