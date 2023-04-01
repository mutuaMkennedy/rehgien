from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from chat.twilio import conversations

# referencing the custom user model
User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_twilio_access_token(request):
    identity = request.user.pk
    token_result = conversations.get_token(identity)

    context = {
    "access_token": token_result,
    }

    return Response(context)
