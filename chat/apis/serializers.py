from rest_framework import serializers
from stream_chat import StreamChat
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_auth.models import TokenModel
from rest_framework_simplejwt.tokens import RefreshToken

# referencing the custom user model
User = get_user_model()


class StreamTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    stream_token = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    tokens_for_user = serializers.SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = ('auth_token','stream_token','tokens_for_user','user_id', 'user_name','user_avatar')

    def get_stream_token(self, obj):
        client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)
        token = client.create_token(str(obj.user.pk))
        return token

    def get_user_id(self, obj):
        return str(obj.user.pk)

    def get_user_name(self, obj):
        return obj.user.username

    def get_user_avatar(self, obj):
        default_avatar = '/static/img/avatar.png'
        if obj.user.profile_image:
            return obj.user.profile_image.url
        else:
            return default_avatar

    def get_tokens_for_user(self, obj):
        """
            We are manually generating the user JWT auth tokens which we will use
            after a successfull user sign up. This will also eliminate the need
            of firing the token request api to get the auth tokens after sign up.
        """
        refresh = RefreshToken.for_user(obj.user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
