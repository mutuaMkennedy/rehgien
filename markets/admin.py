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

class ProjectQuestionInline(admin.StackedInline):
    model = models.ProjectQuestion
    extra=1

class ProjectQuoteInline(admin.StackedInline):
    model = models.ProjectQuote
    extra=1
    max_num =1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectQuoteInline]
    list_display = ("requested_service","project_status","pro_contacted","pro_response_state","publishdate")

class ProjectDetailsAdmin(admin.ModelAdmin):
    inlines = [ProjectQuestionInline]
    list_display = ("project","location")


admin.site.register(models.JobPost, JobPostAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ProjectDetails, ProjectDetailsAdmin)
admin.site.register(models.ProjectQuoteItem)