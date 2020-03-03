from django.shortcuts import render
from listings.models import PropertyForSale, RentalProperty
from listings.apis.serializers import PropertyForSaleSerializer, RentalPropertySerializer
from rest_framework import generics
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


#On Sale view APIS
#listing all for sale property
class ForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.all()
    serializer_class = PropertyForSaleSerializer

#listing all for sale items as per their type/category
class ApartmentsForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Apartment')
    serializer_class = PropertyForSaleSerializer

class MansionsForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Mansion')
    serializer_class = PropertyForSaleSerializer

class BungalowsForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Bungalow')
    serializer_class = PropertyForSaleSerializer

class CondosForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Condominium')
    serializer_class = PropertyForSaleSerializer

class DormsForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Dormitory')
    serializer_class = PropertyForSaleSerializer

class DuplexForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Duplex')
    serializer_class = PropertyForSaleSerializer

class SingleFamilyForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Single family')
    serializer_class = PropertyForSaleSerializer

class TerracedForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Terraced')
    serializer_class = PropertyForSaleSerializer

class TownHouseForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Townhouse')
    serializer_class = PropertyForSaleSerializer

class OthersForSaleListApi(ListAPIView):
    queryset = PropertyForSale.objects.filter(type__iexact='Other')
    serializer_class = PropertyForSaleSerializer

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
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer

#listing all rentals based on their categories
class ApartmentsForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Apartment')
    serializer_class = RentalPropertySerializer

class MansionsForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Mansion')
    serializer_class = RentalPropertySerializer

class BungalowsForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Bungalow')
    serializer_class = RentalPropertySerializer

class CondosForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Condominium')
    serializer_class = RentalPropertySerializer

class DormsForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Dormitory')
    serializer_class = RentalPropertySerializer

class DuplexForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Duplex')
    serializer_class = RentalPropertySerializer

class SingleFamilyForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Single family')
    serializer_class = RentalPropertySerializer

class TerracedForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Terraced')
    serializer_class = RentalPropertySerializer

class TownHouseForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Townhouse')
    serializer_class = RentalPropertySerializer

class OthersForRentListApi(ListAPIView):
    queryset = RentalProperty.objects.filter(type__iexact='Other')
    serializer_class = RentalPropertySerializer

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
