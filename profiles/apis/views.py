from . import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles import models
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView,
                                    DestroyAPIView
                                    )
from rest_framework.views import APIView
from .permissions import (
                        IsUserOrReadOnly,IsOwnerOrReadOnly,AccountOwnerOrReadOnly,
                        IsAPro,IsRequestorOrReceiver,IsProfileOwnerOrReadOnly,
                        IsBusinessProfileOwnerOrReadOnly
                        )
from rest_framework.permissions import (
                                    AllowAny,
                                    IsAuthenticated,
                                    IsAdminUser,
                                    IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response

# referencing the custom user model
User = get_user_model()

class UsersListAPI(ListAPIView):
    serializer_class = serializers.UserAccountSerializer
    queryset = User.objects.all()

class UserAccountEditApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserAccountSerializer
    permission_classes = [AccountOwnerOrReadOnly]

class UserListingsListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class ProfessionalGroupListApi(ListAPIView):
    queryset = models.ProfessionalGroup.objects.all()
    serializer_class = serializers.ProfessionalGroupSerializer

class ProfessionalCategoryListApi(ListAPIView):
    queryset = models.ProfessionalCategory.objects.all()
    serializer_class = serializers.ProfessionalCategorySerializer

class ProfessionalServiceListApi(ListAPIView):
    queryset = models.ProfessionalService.objects.all()
    serializer_class = serializers.ProfessionalServiceSerializer

#Busines profile
class BusinessProfileListApi(ListAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer

class BusinessProfileDetailApi(RetrieveAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer

class BusinessProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.BusinessProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

class SocialBusinessProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.SocialBusinessProfileSerializer
    permission_classes = [IsAuthenticated]

class ReviewListApi(ListAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

class ReviewCreateApi(CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(reviewer=self.request.user)

class LikeReviewUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.LikeReviewSerializer
    permission_classes = [IsAuthenticated]

class LikeReviewUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.LikeReviewSerializer
    permission_classes = [IsAuthenticated]

# Portfolio crud
class PortfolioItemCreateApi(CreateAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer
    permission_classes = [IsAPro]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class PortfolioItemListApi(ListAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer

class PortfolioItemDetailApi(RetrieveAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer

class PortfolioItemUpdateApi(RetrieveUpdateAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

class PortfolioItemDeleteApi(DestroyAPIView):
    queryset = models.PortfolioItem.objects.all()
    serializer_class = serializers.PortfolioItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

# team connection crud
class TeammateConnectionCreate(CreateAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]
    def perform_create(self,serializer):
        serializer.save(requestor=self.request.user)

class TeammateConnectionListApi(ListAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer

class TeammateConnectionDetailApi(RetrieveAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer

class TeammateConnectionUpdateApi(RetrieveUpdateAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]

class TeammateConnectionDeleteApi(DestroyAPIView):
    queryset = models.TeammateConnection.objects.all()
    serializer_class = serializers.TeammateConnectionSerializer
    permission_classes = [IsRequestorOrReceiver]

# Business Hours
class BusinessHoursCreate(CreateAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsAPro]

class BusinessHoursListApi(ListAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer

class BusinessHoursDetailApi(RetrieveAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer

class BusinessHoursUpdateApi(RetrieveUpdateAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

class BusinessHoursDeleteApi(DestroyAPIView):
    queryset = models.BusinessHours.objects.all()
    serializer_class = serializers.BusinessHoursSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

# Client
class ClientCreate(CreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAPro]

class ClientListApi(ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientDetailApi(RetrieveAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientUpdateApi(RetrieveUpdateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]

class ClientDeleteApi(DestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsBusinessProfileOwnerOrReadOnly]
