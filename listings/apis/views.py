from django.shortcuts import render
from listings import models
from listings.apis import serializers
from rest_framework import generics, filters
from django.db.models import Q
from rest_framework.generics import (
                    ListAPIView,
                    CreateAPIView,
                    RetrieveAPIView,
                    RetrieveUpdateAPIView,
                    DestroyAPIView
                    )
from rest_framework.permissions import  (
                    AllowAny,
                    IsAuthenticated,
                    IsAdminUser,
                    IsAuthenticatedOrReadOnly
                    )
from .permissions import IsOwnerOrReadOnly,IsUserOrReadOnly,IsHomeOwnerOrReadOnly
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import django_filters
# referencing the custom user model
User = get_user_model()


class UserHomeListings(ListAPIView):
    serializer_class = serializers.HomeSerializer
    def get_queryset(self):
        """
        This view should return a list of all the Home listings
        for the currently authenticated user.
        """
        user = self.request.user
        return models.Home.objects.filter(owner=user)


#Home model api views
class HomeTypeApi(ListAPIView):
    serializer_class = serializers.HomeTypeSerializer
    queryset = models.HomeType.objects.all()

class HomeFilter(django_filters.FilterSet):
    min_price = django_filters.rest_framework.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.rest_framework.NumberFilter(field_name="price", lookup_expr='lte')
    min_bathrooms = django_filters.rest_framework.NumberFilter(field_name="bathrooms", lookup_expr='gte')
    max_bathrooms = django_filters.rest_framework.NumberFilter(field_name="bathrooms", lookup_expr='lte')
    min_bedrooms = django_filters.rest_framework.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    max_bedrooms = django_filters.rest_framework.NumberFilter(field_name="bedrooms", lookup_expr='lte')
    min_floor_area = django_filters.rest_framework.NumberFilter(field_name="floor_area", lookup_expr='gte')
    max_floor_area = django_filters.rest_framework.NumberFilter(field_name="floor_area", lookup_expr='lte')
    location_name = django_filters.rest_framework.CharFilter(field_name="location_name", lookup_expr='icontains')
    home_type = django_filters.rest_framework.CharFilter(field_name="home_type__name", lookup_expr='icontains')
    class Meta:
        model = models.Home
        fields = {
            'listing_type', 'price', 'property_category',
            'home_type','bathrooms','bedrooms','location_name','floor_area',
        }

class HomeListApi(ListAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = HomeFilter
    ordering_fields  = ['publishdate','floor_area','bathrooms','bedrooms','price']

# Uses a different serializer which does not nest property photo and video table in the response
# which were raising issues in multi file uploads. Media files are uploaded
# with a separate api
class HomeCreateApi(CreateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer2
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class HomeDetailApi(RetrieveAPIView):
    queryset =  models.Home.objects.all()
    serializer_class = serializers.HomeSerializer

# Uses a different serializer which does not nest property photo and video table in the response
# which were raising issues in multi file uploads. Media files are uploaded
# with a separate api
class HomeUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer2
    permission_classes = [IsOwnerOrReadOnly]

class HomeSavesSerializer(RetrieveUpdateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSavesSerializer
    permission_classes = [IsAuthenticated]

class HomeDeleteApi(DestroyAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [IsAuthenticated]

#Home photo api views
class PropertyPhotoListApi(ListAPIView):
    queryset = models.PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer

class PropertyPhotoCreateApi(CreateAPIView):
    queryset = models.PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer
    permission_classes = [IsAuthenticated]

class PropertyPhotoDetailApi(RetrieveAPIView):
    queryset =  models.PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer

class PropertyPhotoUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer
    permission_classes = [IsHomeOwnerOrReadOnly]

class PropertyPhotoDeleteApi(DestroyAPIView):
    queryset = models.PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer
    permission_classes = [IsHomeOwnerOrReadOnly]

#Home video api views
class PropertyVideoListApi(ListAPIView):
    queryset = models.PropertyVideo.objects.all()
    serializer_class = serializers.PropertyVideoSerializer

class PropertyVideoCreateApi(CreateAPIView):
    queryset = models.PropertyVideo.objects.all()
    serializer_class = serializers.PropertyVideoSerializer
    permission_classes = [IsAuthenticated]

class PropertyVideoDetailApi(RetrieveAPIView):
    queryset =  models.PropertyVideo.objects.all()
    serializer_class = serializers.PropertyVideoSerializer

class PropertyVideoUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PropertyVideo.objects.all()
    serializer_class = serializers.PropertyVideoSerializer
    permission_classes = [IsHomeOwnerOrReadOnly]

class PropertyVideoDeleteApi(DestroyAPIView):
    queryset = models.PropertyVideo.objects.all()
    serializer_class = serializers.PropertyVideoSerializer
    permission_classes = [IsHomeOwnerOrReadOnly]

# Property interactions api views
class PropertyInteractionListApi(ListAPIView):
    queryset = models.PropertyInteraction.objects.all()
    serializer_class = serializers.PropertyInteractionSerializer

class PropertyInteractionCreateApi(CreateAPIView):
    queryset = models.PropertyInteraction.objects.all()
    serializer_class = serializers.PropertyInteractionSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class PropertyInteractionDetailApi(RetrieveAPIView):
    queryset =  models.PropertyInteraction.objects.all()
    serializer_class = serializers.PropertyInteractionSerializer

class PropertyInteractionUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PropertyInteraction.objects.all()
    serializer_class = serializers.PropertyInteractionSerializer
    permission_classes = [IsUserOrReadOnly]

class PropertyInteractionDeleteApi(DestroyAPIView):
    queryset = models.PropertyInteraction.objects.all()
    serializer_class = serializers.PropertyInteractionSerializer
    permission_classes = [IsAuthenticated]

class PropertyOpenHouseListApi(ListAPIView):
    queryset = models.PropertyOpenHouse.objects.all()
    serializer_class = serializers.PropertyOpenHouseSerializer

class PropertyOpenHouseCreateApi(CreateAPIView):
    queryset = models.PropertyOpenHouse.objects.all()
    serializer_class = serializers.PropertyOpenHouseSerializer
    permission_classes = [IsAuthenticated]

class PropertyOpenHouseDetailApi(RetrieveAPIView):
    queryset =  models.PropertyOpenHouse.objects.all()
    serializer_class = serializers.PropertyOpenHouseSerializer

class PropertyOpenHouseUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PropertyOpenHouse.objects.all()
    serializer_class = serializers.PropertyOpenHouseSerializer
    permission_classes = [IsAuthenticated]

class PropertyOpenHouseDeleteApi(DestroyAPIView):
    queryset = models.PropertyOpenHouse.objects.all()
    serializer_class = serializers.PropertyOpenHouseSerializer
    permission_classes = [IsAuthenticated]
