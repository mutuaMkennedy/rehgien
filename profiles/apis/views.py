from .serializers import (
                        UserSerializer,
                        UserAccountSerializer,
                        CompanyProfileSerializer,
                        CompanyReviewsSerializer,
                        AgentProfileSerializer,
                        PropertyManagerProfileSerializer,
                        DesignAndServiceProProfileSerializer,
                        AgentReviewsSerializer,
                        PropertyManagerReviewsSerializer,
                        DesignAndServiceProReviewsSerializer,
                        PMPortfolioSerializer,
                        DesignAndServiceProProjectsSerializer,
                        TeammateConnectionSerializer,
                            )
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profiles.models import (
                            CompanyProfile,
                            CompanyReviews,
                            AgentProfile,
                            AgentReviews,
                            PropertyManagerProfile,
                            PropertyManagerReviews,
                            DesignAndServiceProProfile,
                            DesignAndServiceProReviews,
                            PMPortfolio,
                            DesignAndServiceProProjects,
                            TeammateConnection,
                                    )
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView,
                                    DestroyAPIView
                                    )
from .permissions import IsUserOrReadOnly,IsOwnerOrReadOnly,AccountOwnerOrReadOnly,IsAPro
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
    permission_classes = [AccountOwnerOrReadOnly]


class UserListingsListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Company profile
class CompanyProfileListApi(ListAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

class CompanyProfileDetailApi(RetrieveAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

class CompanyProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsUserOrReadOnly]

class CompanyReviewsListApi(ListAPIView):
    queryset = CompanyReviews.objects.all()
    serializer_class = CompanyReviewsSerializer

class CompanyReviewsCreateApi(CreateAPIView):
    queryset = CompanyReviews.objects.all()
    serializer_class = CompanyReviewsSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

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
    permission_classes = [IsUserOrReadOnly]

class AgentReviewsListApi(ListAPIView):
    queryset = AgentReviews.objects.all()
    serializer_class = AgentReviewsSerializer

class AgentReviewsCreateApi(CreateAPIView):
    queryset = AgentReviews.objects.all()
    serializer_class = AgentReviewsSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsUserOrReadOnly]

class PropertyManagerReviewsListApi(ListAPIView):
    queryset = PropertyManagerReviews.objects.all()
    serializer_class = PropertyManagerReviewsSerializer

class PropertyManagerReviewsCreateApi(CreateAPIView):
    queryset = PropertyManagerReviews.objects.all()
    serializer_class = PropertyManagerReviewsSerializer
    permission_classes = []
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

# ds profile
class DesignAndServiceProProfileListApi(ListAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer

class DesignAndServiceProProfileDetailApi(RetrieveAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer

class DesignAndServiceProProfileUpdateApi(RetrieveUpdateAPIView):
    queryset = DesignAndServiceProProfile.objects.all()
    serializer_class = DesignAndServiceProProfileSerializer
    permission_classes = [IsAdminUser]

class DesignAndServiceProReviewsListApi(ListAPIView):
    queryset = DesignAndServiceProReviews.objects.all()
    serializer_class = DesignAndServiceProReviewsSerializer

class DesignAndServiceProReviewsCreateApi(CreateAPIView):
    queryset = DesignAndServiceProReviews.objects.all()
    serializer_class = DesignAndServiceProReviewsSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

# Property Management portfolio CRUD
class PMPortfolioCreateApi(CreateAPIView):
    queryset = PMPortfolio.objects.all()
    serializer_class = PMPortfolioSerializer
    permission_classes = [IsAPro]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class PMPortfolioListApi(ListAPIView):
    queryset = PMPortfolio.objects.all()
    serializer_class = PMPortfolioSerializer

class PMPortfolioDetailApi(RetrieveAPIView):
    queryset = PMPortfolio.objects.all()
    serializer_class = PMPortfolioSerializer

class PMPortfolioUpdateApi(RetrieveUpdateAPIView):
    queryset = PMPortfolio.objects.all()
    serializer_class = PMPortfolioSerializer
    permission_classes = [IsOwnerOrReadOnly]

class PMPortfolioDeleteApi(DestroyAPIView):
    queryset = PMPortfolio.objects.all()
    serializer_class = PMPortfolioSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Designers & service providers portfolio CRUD
class DesignAndServiceProProjectsApi(CreateAPIView):
    queryset = DesignAndServiceProProjects.objects.all()
    serializer_class = DesignAndServiceProProjectsSerializer
    permission_classes = [IsAPro]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class DesignAndServiceProProjectsListApi(ListAPIView):
    queryset = DesignAndServiceProProjects.objects.all()
    serializer_class = DesignAndServiceProProjectsSerializer

class DesignAndServiceProProjectsDetailApi(RetrieveAPIView):
    queryset = DesignAndServiceProProjects.objects.all()
    serializer_class = DesignAndServiceProProjectsSerializer

class DesignAndServiceProProjectsUpdateApi(RetrieveUpdateAPIView):
    queryset = DesignAndServiceProProjects.objects.all()
    serializer_class = DesignAndServiceProProjectsSerializer
    permission_classes = [IsOwnerOrReadOnly]

class DesignAndServiceProProjectsDeleteApi(DestroyAPIView):
    queryset = DesignAndServiceProProjects.objects.all()
    serializer_class = DesignAndServiceProProjectsSerializer
    permission_classes = [IsOwnerOrReadOnly]

# team connection crud
class TeammateConnectionApi(CreateAPIView):
    queryset = TeammateConnection.objects.all()
    serializer_class = TeammateConnectionSerializer
    permission_classes = [IsAPro]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class TeammateConnectionListApi(ListAPIView):
    queryset = TeammateConnection.objects.all()
    serializer_class = TeammateConnectionSerializer

class TeammateConnectionDetailApi(RetrieveAPIView):
    queryset = TeammateConnection.objects.all()
    serializer_class = TeammateConnectionSerializer

class TeammateConnectionUpdateApi(RetrieveUpdateAPIView):
    queryset = TeammateConnection.objects.all()
    serializer_class = TeammateConnectionSerializer
    permission_classes = [IsOwnerOrReadOnly]

class TeammateConnectionDeleteApi(DestroyAPIView):
    queryset = TeammateConnection.objects.all()
    serializer_class = TeammateConnectionSerializer
    permission_classes = [IsOwnerOrReadOnly]
