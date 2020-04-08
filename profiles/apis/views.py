from .serializers import UserProfileSerializer
from django.contrib.auth.models import User
from profiles.models import UserProfile
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from .permissions import IsUserOrReadOnly
from rest_framework.permissions import IsAdminUser


class UserProfileView(ListAPIView):
    serializer_class = UserProfileSerializer
    def get_queryset(self):
        """
        This view should return a the profile
        for the currently authenticated user.
        """
        user = self.request.user
        return UserProfile.objects.filter(user=user)

class ProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]
