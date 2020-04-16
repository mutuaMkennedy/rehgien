from .serializers import UserProfileSerializer,UserSerializer,UserAccountSerializer
from django.contrib.auth.models import User
from profiles.models import UserProfile
from rest_framework.generics import (
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView
                                    )
from .permissions import IsUserOrReadOnly,AccountOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser


class UsersListAPI(ListAPIView):
    serializer_class = UserAccountSerializer
    queryset = User.objects.all()

class UserAccountEditApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AccountOwnerOrReadOnly,IsAdminUser]

class UserProfileView(ListAPIView):
    serializer_class = UserProfileSerializer
    def get_queryset(self):
        """
        This view should return a the profile
        for the currently authenticated user.
        """
        user = self.request.user
        return UserProfile.objects.filter(user=user)


class ProfileListApi(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ProfileDetailApi(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]

class UserListingsListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
