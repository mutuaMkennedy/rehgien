from django.shortcuts import render
from listings import models
from listings.apis import serializers
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
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

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
class PropertyTypeImageList(ListAPIView):
    serializer_class = serializers.PropertyTypeImageSerializer
    queryset = models.PropertyTypeImage.objects.all()

class HomeListApi(ListAPIView):
    serializer_class = serializers.HomeSerializer
    filter_backends = [SearchFilter]
    search_fields = [ 'listing_type','type']

    def get_queryset(self,*args,**kwargs):
        queryset_list = models.Home.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list=queryset_list.filter(
            Q(type__icontains=query)
            ).distinct()
        return queryset_list

class HomeCreateApi(CreateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class HomeDetailApi(RetrieveAPIView):
    queryset =  models.Home.objects.all()
    serializer_class = serializers.HomeSerializer

class HomeUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [IsOwnerOrReadOnly]

class HomeSavesSerializer(RetrieveUpdateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSavesSerializer
    permission_classes = [IsAuthenticated]

class HomeDeleteApi(DestroyAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [IsAuthenticated]
