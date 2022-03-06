from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
from markets import models
from profiles import models as profile_models
from django.db.models import Avg
from profiles.apis import serializers as profile_serializers
from location.api import serializers as location_serializers

# referencing the custom user model
User = get_user_model()

class JobPostProposalSerializer(serializers.ModelSerializer):
    proposal_sender_object = serializers.SerializerMethodField()
    class Meta:
        model = models.JobPostProposal
        fields = [
        "pk", "job_post","message","proposal_sender","proposal_send_date",
        "proposal_sender_object"
        ]

    def get_proposal_sender_object(self,obj):
        business_page_rating = obj.proposal_sender.pro_business_profile.pro_business_review.all().aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
        business_page_object = {
            "pk":obj.proposal_sender.pro_business_profile.pk,
            "user":obj.proposal_sender.pro_business_profile.user.username,
            "professional_category":obj.proposal_sender.pro_business_profile.professional_category.category_name,
            "business_profile_image":obj.proposal_sender.pro_business_profile.business_profile_image.url if obj.proposal_sender.pro_business_profile.business_profile_image else '',
            "business_name":obj.proposal_sender.pro_business_profile.business_name,
            "phone":obj.proposal_sender.pro_business_profile.phone,
            "business_email":obj.proposal_sender.pro_business_profile.business_email,
            "pro_average_rating":business_page_rating if business_page_rating else '0'
        }

        user_object = {
            'pk':obj.proposal_sender.pk,
            'username':obj.proposal_sender.username,
            'first_name':obj.proposal_sender.first_name,
            'last_name':obj.proposal_sender.last_name,
            'email':obj.proposal_sender.email,
            'user_type':obj.proposal_sender.user_type,
            'profile_image':obj.proposal_sender.profile_image.url if obj.proposal_sender.profile_image else '',
            'business_page':business_page_object

            }
        return user_object


class JobPostSerializer(serializers.ModelSerializer):
    job_post_proposal = JobPostProposalSerializer(many=True, required=False)
    job_poster_object = serializers.SerializerMethodField()
    job_viewers_object = serializers.SerializerMethodField()
    class Meta:
        model = models.JobPost
        fields = [
        "pk", "title", "description", "project_size", "project_duration",
        "skill_areas", "verified", "active", "location", "job_viewers",
        "job_creation_date", "job_update_date","job_poster","job_poster_object",
        "job_viewers_object", "job_post_proposal"
        ]

    def get_job_poster_object(self,obj):
        user_object = {
            'pk':obj.job_poster.pk,
            'username':obj.job_poster.username,
            'first_name':obj.job_poster.first_name,
            'last_name':obj.job_poster.last_name,
            'email':obj.job_poster.email,
            'user_type':obj.job_poster.user_type,
            'profile_image':obj.job_poster.profile_image.url if obj.job_poster.profile_image else '',
            }
        return user_object

    def get_job_viewers_object(self,obj):
        user_array = []
        for usr in obj.job_viewers.all():
            user_object = {
                'pk':usr.pk,
                'username':usr.username,
                'first_name':usr.first_name,
                'last_name':usr.last_name,
                'email':usr.email,
                'user_type':usr.user_type,
                'profile_image':usr.profile_image.url if usr.profile_image else '',
                }
            user_array.append(user_object)
        return user_array

class JobPostViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPost
        fields = ['job_viewers']

class ProjectQuestionSerializer(WritableNestedModelSerializer):
    question_object = serializers.SerializerMethodField()
    answer_object = serializers.SerializerMethodField()
    class Meta:
        model = models.ProjectQuestion
        fields = [
        "pk","project_details","question","answer","question_object","answer_object"
        ]

    def get_question_object(self, object):
        question = object.question
        return profile_serializers.QuestionSerializer(question).data

    def get_answer_object(self, object):
        answer = object.answer
        return profile_serializers.QuestionOptionsSerializer(answer, many=True).data

class ProjectDetailsSerializer(WritableNestedModelSerializer):
    project_questions = ProjectQuestionSerializer(many=True)
    location_object = serializers.SerializerMethodField()
    class Meta:
        model = models.ProjectDetails
        fields = [
        "pk","project","location","location_object","project_questions"
        ]

    def get_location_object(self, object):
        location = object.location
        return location_serializers.KenyaTownSerializer(location).data

class ProjectQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectQuote
        fields = [
        "pk","project","message","price","negotiable","quote_sender","quote_send_date",
        ]

class ProjectSerializer(WritableNestedModelSerializer):
    project_details = ProjectDetailsSerializer(many=True, required=False)
    project_quote = ProjectQuoteSerializer(many=True, required=False)
    owner = serializers.SerializerMethodField()
    pro_contacted_object = serializers.SerializerMethodField()
    requested_service_object = serializers.SerializerMethodField()
    class Meta:
        model = models.Project
        fields = [
        "RESPONSE_STATE","PROJECT_STATE","pk","owner","client_message","requested_service","requested_service_object", "project_status",
        "pro_contacted","pro_contacted_object", "pro_response_state","publishdate",
        "project_details", "project_quote",
        ]

    def get_owner(self, object):
        user = object.owner
        return profile_serializers.UserSerializer(user).data

    def get_pro_contacted_object(self, object):
        pro = object.pro_contacted.pro_business_profile
        return profile_serializers.BusinessProfileSerializer(pro).data

    def get_requested_service_object(self, object):
        service = object.requested_service
        return profile_serializers.ProfessionalServiceSerializer(service).data
