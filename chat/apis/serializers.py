from rest_framework import serializers
from stream_chat import StreamChat
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_auth.models import TokenModel
# referencing the custom user model
User = get_user_model()


class StreamTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    stream_token = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = ('auth_token','stream_token','user_id', 'user_name','user_avatar')

    def get_stream_token(self, obj):
        client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)
        token = client.create_token(str(obj.user.pk))
        return token

    def get_user_id(self, obj):
        return str(obj.user.pk)

    def get_user_name(self, obj):
        return obj.user.username

    def get_user_avatar(self, obj):
        if obj.user.user_type =='NormalUser':
            return obj.user.n_user_profile.profile_image.url
        if obj.user.user_type =='Agent':
            return obj.user.agent_profile.profile_image.url
        if obj.user.user_type =='PropertyManager':
            return obj.user.pm_profile.profile_image.url
        if obj.user.user_type =='Design&servicePro':
            return obj.user.DService_profile.profile_image.url
        if obj.user.user_type =='Admin':
            return obj.user.agent_profile.profile_image.url
