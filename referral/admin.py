from django.contrib import admin
from . import models


class ReferralPayoutsInline(admin.StackedInline):
	model = models.ReferralPayouts
	extra = 1

class RecruiterAdmin(admin.ModelAdmin):
    inlines = [ReferralPayoutsInline]
    list_display = ("recruiter", "referral_code")

admin.site.register(models.Recruiter, RecruiterAdmin)
admin.site.register(models.ReferralSystem)