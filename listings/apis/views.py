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
from .permissions import IsOwnerOrReadOnly,IsUserOrReadOnly
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
class HomeTypeApi(ListAPIView):
    serializer_class = serializers.HomeTypeSerializer
    queryset = models.HomeType.objects.all()

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
