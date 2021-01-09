from django.contrib import admin
from . import models

class JobPostInline(admin.StackedInline):
    model = models.JobPostProposal

class JobPostAdmin(admin.ModelAdmin):
    inlines = [JobPostInline]
    list_display = (
        "title", "project_size", "project_duration", "location",
        "verified","active",
    )

admin.site.register(models.JobPost, JobPostAdmin)
