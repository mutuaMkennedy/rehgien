from django.shortcuts import render
from listings.models import (
                    PropertyForSale,
                    RentalProperty,
                    PropertyForSaleImages,
                    PropertyForSaleVideos,
                    RentalImages,
                    RentalVideos
                    )
from listings.apis.serializers import (
                    PropertyForSaleSerializer,
                    RentalPropertySerializer,
                    PropertyForSaleImagesSerializer,
                    PropertyForSaleVideosSerializer,
                    RentalImagesSerializer,
                    RentalVideosSerializer,
                    UserSerializer
                    )
from rest_framework import generics
from rest_framework.filters import SearchFilter
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
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

#USERS VIEW

class UsersList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

#On Sale view APIS
#listing all for sale property
class ForSaleListApi(ListAPIView):
    # queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['type']

    def get_queryset(self,*args,**kwargs):
        queryset_list =PropertyForSale.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list=queryset_list.filter(
            Q(type__icontains=query)
            ).distinct()
        return queryset_list

#creating a for sale listing
class ForSaleCreateApi(CreateAPIView):
    queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

#Retrieving details of a specific for sale listing
class ForSaleDetailApi(RetrieveAPIView):
    queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer

#Updating details of a specific for sale listing
class ForSaleUpdateApi(RetrieveUpdateAPIView):
    queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

#Deleting a for sale listing
class ForSaleDeleteApi(DestroyAPIView):
    queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

#RENTALS APIS
#listing all for rent property
class ForRentListApi(ListAPIView):
    # queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
    filter_backends = [SearchFilter]
    search_fields = ['type']
    def get_queryset(self,*args,**kwargs):
        queryset_list =RentalProperty.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list=queryset_list.filter(
            Q(type__icontains=query)
            ).distinct()
        return queryset_list

class ForRentCreateApi(CreateAPIView):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

#Retrieving details of a specific rental listing
class ForRentDetailApi(RetrieveAPIView):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer

#Updating details of a specific for rent listing
class ForRentUpdateApi(RetrieveUpdateAPIView):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

#Retrieving details of a specific rental listing
class ForRentDeleteApi(DestroyAPIView):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
