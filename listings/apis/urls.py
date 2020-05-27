from django.urls import path, include
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from listings.apis.views import (
                PropertyTypeImageList,
                ForSaleListApi,
                ForSaleCreateApi,
                ForSaleDetailApi,
                ForSaleUpdateApi,
                ForSaleDeleteApi,
                ForRentListApi,
                ForRentCreateApi,
                ForRentDetailApi,
                ForRentUpdateApi,
                ForRentDeleteApi,
                UsersList,
                UserSalePosts,
                UserRentalPosts
                )
# from rest_framework import routers
#
# router=routers.DefaultRouter()
# router.register('OnsaleListings', views.onSaleViewSet())

urlpatterns = [
    path('listings/propertyTypeImages/', PropertyTypeImageList.as_view(), name='p_type_list_api'),
    #for sale url endpoints
    path('listings/for-sale/', ForSaleListApi.as_view(), name='for_sale_list_api'),
    path('listings/for-sale/create/', ForSaleCreateApi.as_view(), name='onsale_create_api'),
    url(r'^listings/for-sale/(?P<pk>[0-9]+)/$', ForSaleDetailApi.as_view(), name='onsale_detail_api'),
    path('listings/for-sale/<int:pk>/edit/', ForSaleUpdateApi.as_view(), name='onsale_update_api'),
    path('listings/for-sale/<int:pk>/delete/', ForSaleDeleteApi.as_view(), name='onsale_delete_api'),
    #rental url endpoints
    path('listings/for-rent/', ForRentListApi.as_view(), name='rentals_list_api'),
    path('listings/for-rent/create/', ForRentCreateApi.as_view(), name='rentals_create_api'),
    url(r'^listings/for-rent/(?P<pk>[0-9]+)/$', ForRentDetailApi.as_view(), name='rentals_detail_api'),
    path('listings/for-rent/<int:pk>/edit/', ForRentUpdateApi.as_view(), name='rentals_update_api'),
    path('listings/for-rent/<int:pk>/delete/', ForRentDeleteApi.as_view(), name='rentals_delete_api'),
    #Users & authentication
    path('accounts/users/', UsersList.as_view(), name='users'), #will be removed . diplicate of users_list in profiles app
    path('accounts/user/listings/for-sale/', UserSalePosts.as_view(), name='user_sale_posts'),
    path('accounts/user/listings/rentals/', UserRentalPosts.as_view(), name='user_rental_posts'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
