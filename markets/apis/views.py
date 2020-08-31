from django.shortcuts import render
from markets.apis.serializers import (
                    PropertyRequestLeadSerializer,
                    ProffesionalRequestLeadSerializer,
                    OtherServiceLeadSerializer,
                    AgentLeadRequestSerializer,
                    AgentPropertyRequestSerializer,
                    ClaimReferPropertyRequestLeadSerializer,
                    ClaimReferProRequestLeadSerializer,
                    ClaimReferOtherServiceLeadSerializer,
                    ClaimReferAgentLeadRequestSerializer,
                    ClaimReferAgentPropertyRequestSerializer,
                    )
from markets.models import (
        PropertyRequestLead,
        ProffesionalRequestLead,
        OtherServiceLead,
        AgentLeadRequest,
        AgentPropertyRequest,
                )
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
from django.contrib.auth import get_user_model

# referencing the custom user model
User = get_user_model()

# PropertyRequestLead CRUD
class PropertyRequestLeadApi(ListAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = PropertyRequestLeadSerializer

class PropertyRequestLeadCreateApi(CreateAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = PropertyRequestLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class PropertyRequestLeadDetailApi(RetrieveAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = PropertyRequestLeadSerializer

class PropertyRequestLeadUpdateApi(RetrieveUpdateAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = PropertyRequestLeadSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

class ClaimReferPropertyRequestLeadApi(RetrieveUpdateAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = ClaimReferPropertyRequestLeadSerializer
    # permission_classes = [IsAuthenticated]

class PropertyRequestLeadDeleteApi(DestroyAPIView):
    queryset = PropertyRequestLead.objects.all()
    serializer_class = PropertyRequestLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

# proffesional Request CRUD
class ProffesionalRequestLeadApi(ListAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ProffesionalRequestLeadSerializer

class ProffesionalRequestLeadCreateApi(CreateAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ProffesionalRequestLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class ProffesionalRequestLeadDetailApi(RetrieveAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ProffesionalRequestLeadSerializer

class ProffesionalRequestLeadUpdateApi(RetrieveUpdateAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ProffesionalRequestLeadSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

class ClaimReferProRequestLeadApi(RetrieveUpdateAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ClaimReferProRequestLeadSerializer
    # permission_classes = [IsAuthenticated]

class ProffesionalRequestLeadDeleteApi(DestroyAPIView):
    queryset = ProffesionalRequestLead.objects.all()
    serializer_class = ProffesionalRequestLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

#OtherServiceLead CRUD
class OtherServiceLeadApi(ListAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = OtherServiceLeadSerializer

class OtherServiceLeadCreateApi(CreateAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = OtherServiceLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class OtherServiceLeadDetailApi(RetrieveAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = OtherServiceLeadSerializer

class OtherServiceLeadUpdateApi(RetrieveUpdateAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = OtherServiceLeadSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

class ClaimReferOtherServiceLeadApi(RetrieveUpdateAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = ClaimReferOtherServiceLeadSerializer
    # permission_classes = [IsAuthenticated]

class OtherServiceLeadDeleteApi(DestroyAPIView):
    queryset = OtherServiceLead.objects.all()
    serializer_class = OtherServiceLeadSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

#AgentLeadRequest CRUD
class AgentLeadRequestApi(ListAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = AgentLeadRequestSerializer

class AgentLeadRequestCreateApi(CreateAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = AgentLeadRequestSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class AgentLeadRequestDetailApi(RetrieveAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = AgentLeadRequestSerializer

class AgentLeadRequestUpdateApi(RetrieveUpdateAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = AgentLeadRequestSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

class ClaimReferAgentLeadRequestApi(RetrieveUpdateAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = ClaimReferAgentLeadRequestSerializer
    # permission_classes = [IsAuthenticated]

class AgentLeadRequestDeleteApi(DestroyAPIView):
    queryset = AgentLeadRequest.objects.all()
    serializer_class = AgentLeadRequestSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

#AgentPropertyRequest CRUD
class AgentPropertyRequestApi(ListAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = AgentPropertyRequestSerializer

class AgentPropertyRequestCreateApi(CreateAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = AgentPropertyRequestSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class AgentPropertyRequestDetailApi(RetrieveAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = AgentPropertyRequestSerializer

class AgentPropertyRequestUpdateApi(RetrieveUpdateAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = AgentPropertyRequestSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAdminUser]

class ClaimReferAgentPropertyRequestApi(RetrieveUpdateAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = ClaimReferAgentPropertyRequestSerializer
    # permission_classes = [IsAuthenticated]

class AgentPropertyRequestDeleteApi(DestroyAPIView):
    queryset = AgentPropertyRequest.objects.all()
    serializer_class = AgentPropertyRequestSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
