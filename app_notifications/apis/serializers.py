from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
from markets import models as markets_models
from app_notifications import models
from django.db.models import Avg
from profiles.apis import serializers as profile_serilizers
from markets.apis import serializers as markets_serilizers
from notifications.models import Notification

# referencing the custom user model
User = get_user_model()

class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, markets_models.Project):
            serializer = markets_serilizers.ProjectSerializer(value)

        return serializer.data


class NotificationSerializer(WritableNestedModelSerializer):
    recipient = profile_serilizers.UserSerializer(User, read_only=True)
    source = serializers.SerializerMethodField()
    target = GenericNotificationRelatedField(read_only=True)
    class Meta:
        model = Notification
        fields = "__all__"

    def get_source(self,obj):
        quote = markets_models.ProjectQuote.objects.filter(id=obj.actor_object_id)
        return markets_serilizers.ProjectQuoteSerializer(quote.first(),read_only=True).data

class DeviceInformationSerializer(WritableNestedModelSerializer):
    # user = profile_serilizers.UserSerializer(User)
    class Meta:
        model = models.DeviceInformation
        fields = "__all__"
