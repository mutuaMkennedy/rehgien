from . import serializers
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
from . import permissions
from app_notifications import models
from notifications.models import Notification

class NotificationsListApi(ListAPIView):
    serializer_class = serializers.NotificationSerializer
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user)

class NotificationsUpdateApi(RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsRecipient]

class DeviceInformationListApi(ListAPIView):
    serializer_class = serializers.DeviceInformationSerializer
    def get_queryset(self):
        user = self.request.user
        return models.DeviceInformation.objects.filter(user=user)

class DeviceInformationCreateApi(CreateAPIView):
    queryset = models.DeviceInformation.objects.all()
    serializer_class = serializers.DeviceInformationSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class DeviceInformationUpdateApi(RetrieveUpdateAPIView):
    queryset = models.DeviceInformation.objects.all()
    serializer_class = serializers.DeviceInformationSerializer
    permission_classes = [permissions.IsUser]

class SupportedAppVersionListApi(ListAPIView):
    serializer_class = serializers.SupportedAppVersionSerializer
    queryset = models.SupportedAppVersion.objects.all()