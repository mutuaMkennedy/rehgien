from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
from django.db.models import Avg
from contact import models

# referencing the custom user model
User = get_user_model()

class PageReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageReport
        fields = ["id","problem_choices","problem","email","details",
        "subject_user_id","resolved",
        ]

class PortfolioReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectsPortfolioReport
        fields = ["id","problem_choices","problem","email","details",
        "subject_user_id","subject_item_id","resolved",
        ]

class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewReport
        fields = ['id','problem_choices','problem','email','details','subject_user_id',
        'subject_item_id','resolved',]
