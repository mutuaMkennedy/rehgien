from markets import models as markets_models
from markets.apis import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

# referencing the custom user model
User = get_user_model()


@api_view(['GET'])
def LeadsListApi(request):
    user = request.user
    if user.user_type == 'PRO':
        leads = markets_models.Project.objects.filter(pro_contacted=user)
        serializer = serializers.ProjectSerializer(leads,many=True)
        return Response(serializer.data)
    else:
        message = {'Unauthorized': 'Your account is not authorized to access this API'}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)