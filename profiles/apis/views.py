from .serializers import (
                        UserSerializer,
                        UserAccountSerializer,
                        NormalUserProfileSerializer,
                        AgentProfileSerializer,
                        PropertyManagerProfileSerializer,
                        DesignAndServiceProProfileSerializer,
                        AgentReviewsSerializer,
                        PropertyManagerReviewsSerializer,
                        DesignAndServiceProReviewsSerializer
                            )
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles.models import (
                            NormalUserProfile,
                            AgentProfile,
                            AgentReviews,
                            PropertyManagerProfile,
                            PropertyManagerReviews,
                            DesignAndServiceProProfile,
                            DesignAndServiceProReviews
                                    )
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView
                                    )
from .permissions import IsUserOrReadOnly,AccountOwnerOrReadOnly
from rest_framework.permissions import (
                                    AllowAny,
                                    IsAuthenticated,
                                    IsAdminUser,
                                    IsAuthenticatedOrReadOnly
                                        )

# referencing the custom user model
User = get_user_model()

class UsersListAPI(ListAPIView):
    serializer_class = UserAccountSerializer
    queryset = User.objects.all()

class UserAccountEditApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AccountOwnerOrReadOnly,IsAdminUser]

#remove this on next commit
class UserProfileView(ListAPIView):
    serializer_class = AgentProfileSerializer
    def get_queryset(self):
        """
        This view should return a the profile
        for the currently authenticated user.
        """
        user = self.request.user
        return AgentProfile.objects.filter(user=user)

class UserListingsListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Normal users profiles
class NormalUserProfileListApi(ListAPIView):
    queryset = NormalUserProfile.objects.all()
    serializer_class = NormalUserProfileSerializer

class NormalUserProfileDetailApi(RetrieveAPIView):
    queryset = NormalUserProfile.objects.all()
    serializer_class = NormalUserProfileSerializer

class NormalUserProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = NormalUserProfile.objects.all()
    serializer_class = NormalUserProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]

# Agent profile
class AgentProfileListApi(ListAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer

class AgentProfileDetailApi(RetrieveAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer

class AgentProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]

class AgentReviewsListApi(ListAPIView):
    queryset = AgentReviews.objects.all()
    serializer_class = AgentReviewsSerializer

class AgentReviewsCreateApi(CreateAPIView):
    queryset = AgentReviews.objects.all()
    serializer_class = AgentReviewsSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

# property manager profile
class PropertyManagerProfileListApi(ListAPIView):
    queryset = PropertyManagerProfile.objects.all()
    serializer_class = PropertyManagerProfileSerializer

class PropertyManagerProfileDetailApi(RetrieveAPIView):
    queryset = PropertyManagerProfile.objects.all()
    serializer_class = PropertyManagerProfileSerializer

class PropertyManagerProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = PropertyManagerProfile.objects.all()
    serializer_class = PropertyManagerProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]

class PropertyManagerReviewsListApi(ListAPIView):
    queryset = PropertyManagerReviews.objects.all()
    serializer_class = PropertyManagerReviewsSerializer

class PropertyManagerCreateApi(CreateAPIView):
    queryset = PropertyManagerReviews.objects.all()
    serializer_class = PropertyManagerReviewsSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

# property manager profile
class DesignAndServiceProProfileListApi(ListAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer

class DesignAndServiceProProfileDetailApi(RetrieveAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer

class DesignAndServiceProProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer
    permission_classes = [IsUserOrReadOnly,IsAdminUser]

class DesignAndServiceProReviewsListApi(ListAPIView):
    queryset = DesignAndServiceProReviews.objects.all()
    serializer_class = DesignAndServiceProReviewsSerializer

class DesignAndServiceProReviewsCreateApi(CreateAPIView):
    queryset = DesignAndServiceProReviews.objects.all()
    serializer_class = DesignAndServiceProReviewsSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
