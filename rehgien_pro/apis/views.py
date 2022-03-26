from markets import models as markets_models
from profiles import models as profiles_models
from markets.apis import serializers
from profiles.apis import serializers as profiles_serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import permissions 
from rest_framework.permissions import  (
                    IsAuthenticated,
                    )
from django.contrib.auth import get_user_model
from ..views import send_review_request_email

# referencing the custom user model
User = get_user_model()


@api_view(['GET'])
def LeadsListApi(request):
    user = request.user
    if user.user_type == 'PRO':
        leads = markets_models.Project.objects.filter(pro_contacted=user).order_by('-publishdate')
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

def update_pro_answers(user, questions):
    bs_profile = profiles_models.BusinessProfile.objects.filter(user=user.pk)
    if bs_profile.exists():
        for q in questions:
            selected_options = ''
            question_id = ''
            try:
                selected_options = q['answer']
                question_id = q['question_id']
            except:
                pass
            if question_id and selected_options:
                pro_answer = profiles_models.ProAnswer.objects.filter(business_profile = bs_profile.first().pk, question = question_id)
                question_obj = profiles_models.Question.objects.filter(pk=question_id)

                if pro_answer.exists():
                    """There is a answer object. So update it"""
                    instance = pro_answer.first()
                    instance.answer.set(selected_options)
                else:
                    """There is no answer yet. So create one"""
                    if question_obj.exists():
                        """Ignore questions that don't exist"""
                        instance = profiles_models.ProAnswer.objects.create(
                        business_profile = bs_profile,
                        question = question_obj.first()
                        )
                        instance.answer.set(selected_options)
            else:
                context = {
                    "status":False,
                    "question": [{
                        "question_id": ["This field is required"],
                        "answer": ["This field is required"]
                    }]
                    }
                return context
                
        context = {
            "status":True,
            "details": "Targeting preferences updated sucessfully"
            }
        return context
    else:
        context = {
            "status":False,
            "details": "No business profile found for user"
            }
        return context

def update_pro_answers_service_areas(user,questions,service_areas):
    bs_profile = profiles_models.BusinessProfile.objects.filter(user=user.pk)
    if bs_profile.exists():
        for q in questions:
            question_id = ''
            try:
                question_id = q['question_id']
            except:
                pass
            if question_id:
                pro_answer = profiles_models.ProAnswer.objects.filter(business_profile = bs_profile.first().pk, question = question_id)
                question_obj = profiles_models.Question.objects.filter(pk=question_id)

                if pro_answer.exists():
                    """There is a answer object. So update it"""
                    instance = pro_answer.first()
                    instance.service_delivery_areas.set(service_areas)
                else:
                    """There is no answer yet. So create one"""
                    if question_obj.exists():
                        """Ignore questions that don't exist"""
                        instance = profiles_models.ProAnswer.objects.create(
                        business_profile = bs_profile.first(),
                        question = question_obj.first()
                        )
                        instance.service_delivery_areas.set(service_areas)
            else:
                context = {
                    "status":False,
                    "question": [{
                        "question_id": ["This field is required"]
                    }]
                    }
                return context
                
        context = {
            "status":True,
            "details": "Targeting preferences updated sucessfully"
            }
        return context
    else:
        context = {
            "status":False,
            "details": "No business profile found for user"
            }
        return context

@api_view(['POST'])
def update_targeting_preferences(request):
    target = ''
    try:
        target = request.data['target']
    except:
        pass

    if target:
        if target == 'question-answers':
            questions = ""
            try:
                questions = request.data['questions']
            except:
                pass
            
            if questions:
                response = update_pro_answers(request.user, questions)
                if response["status"] == True:
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                "questions":["This field is required"]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        elif target == 'service-areas':
            service_areas = ""
            questions = ""
            try:
                service_areas = request.data['service_areas']
                questions = request.data['questions']
            except:
                pass

            if service_areas:
                response = update_pro_answers_service_areas(request.user, questions,service_areas)
                if response["status"] == True:
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                "questions":["This field is required"],
                "service_areas":["This field is required"]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        else:
            context = {
                "target":["Invalid value for target. Set either question-answers or service-areas"]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {
            "target":["This field is required"]
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_email_review_requests(request):
    emails = ""
    message = ""
    try:
        emails = request.data['emails']
        message = request.data['message']
    except:
        pass

    if emails and message:
        business_profile = request.user.pro_business_profile
        response = send_review_request_email(emails, message, business_profile.pk, business_profile.business_name)
        if response:
            message = {
                'status':True,
                "details": "Emails sent sucessfully"
            }
            return Response(message, status=status.HTTP_200_OK)
    else:
        context = {
        "emails":["This field is required"],
        "message":["This field is required"]
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

class PortfolioItemListApi(generics.ListAPIView):
    queryset = profiles_models.PortfolioItem.objects.all()
    serializer_class = profiles_serializers.PortfolioItemSerializer

class PortfolioItemCreateApi(generics.CreateAPIView):
    queryset = profiles_models.PortfolioItem.objects.all()
    serializer_class = profiles_serializers.PortfolioItemSerializer2
    permission_classes = [permissions.IsAPro2]
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class PortfolioItemUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = profiles_models.PortfolioItem.objects.all()
    serializer_class = profiles_serializers.PortfolioItemSerializer2
    permission_classes = [permissions.IsAPro2]

class PortfolioItemDeleteApi(generics.DestroyAPIView):
    queryset = profiles_models.PortfolioItem.objects.all()
    serializer_class = profiles_serializers.PortfolioItemSerializer2
    permission_classes = [permissions.IsAPro2]

"""
We will currently use different APIs to create/update/delete photos to bypass
an issue of doing crud operations on photos nested in an array
"""
class PortfolioItemPhotoCreateApi(generics.CreateAPIView):
    queryset = profiles_models.PortfolioItemPhoto.objects.all()
    serializer_class = profiles_serializers.PortfolioItemPhotoSerializer
    permission_classes = [permissions.IsOwner]

class PortfolioItemPhotoUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = profiles_models.PortfolioItemPhoto.objects.all()
    serializer_class = profiles_serializers.PortfolioItemPhotoSerializer
    permission_classes = [permissions.IsOwner]

class PortfolioItemPhotoDeleteApi(generics.DestroyAPIView):
    queryset = profiles_models.PortfolioItemPhoto.objects.all()
    serializer_class = profiles_serializers.PortfolioItemPhotoSerializer
    permission_classes = [permissions.IsOwner]