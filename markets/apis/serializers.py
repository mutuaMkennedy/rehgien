from rest_framework import serializers
from django.contrib.auth import get_user_model
from markets import models

# referencing the custom user model
User = get_user_model()

class JobPostProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPostProposal
        fields = '__all__'

class JobPostSerializer(serializers.ModelSerializer):
    job_post_proposal = JobPostProposalSerializer(many=True)
    class Meta:
        model = models.JobPost
        fields = '__all__'

class JobPostViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPost
        fields = ['job_viewers']
