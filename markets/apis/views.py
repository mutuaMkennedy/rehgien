from django.shortcuts import render
from . import serializers
from markets import models
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
from .permissions import IsOwnerOrReadOnly,IsPro
from django.contrib.auth import get_user_model

# referencing the custom user model
User = get_user_model()

# PropertyRequestLead CRUD
class JobPostListApi(ListAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer

class JobPostCreateApi(CreateAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(job_poster=self.request.user)

class JobPostDetailApi(RetrieveAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer

class JobPostUpdateApi(RetrieveUpdateAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class JobPostViewerUpdateApi(RetrieveUpdateAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializers.JobPostViewsSerializer

class JobPostProposalCreateApi(CreateAPIView):
    queryset = models.JobPostProposal.objects.all()
    serializer_class = serializers.JobPostProposalSerializer
    permission_classes = IsPro
    def perform_create(self,serializer):
        serializer.save(proposal_sender=self.request.user)
