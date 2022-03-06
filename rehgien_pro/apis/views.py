from markets import models as markets_models
from markets.apis import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import permissions 
from rest_framework.permissions import  (
                    IsAuthenticated,
                    )
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


class AddQuoteApi(generics.RetrieveUpdateAPIView):
    queryset = markets_models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated, permissions.IsAPro]
    # def perform_update(self,serializer):
    #     print('1')
    #     instance = serializer.save()
    #     instance.project_quote.quote_sender = self.request.user
    #     print('2')
    #     # serializer.save(project_quote__quote_sender=self.request.user)
