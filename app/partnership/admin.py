from django.contrib import admin
from . import models


class RehgienPartnerAdmin(admin.ModelAdmin):
    list_display = [
        "partner_program","first_name","last_name","email","company_name",
        "company_website"
    ]

admin.site.register(models.PartnerProgram)
admin.site.register(models.RehgienPartner, RehgienPartnerAdmin)
