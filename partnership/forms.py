from django import forms
from  . import models

class PartnerForm(forms.ModelForm):
    class Meta:
        model = models.RehgienPartner
        fields = [
            "partner_program","first_name","last_name",
            "email","company_name","company_website","phone_number"
        ]
        widget ={
        "partner_program":forms.RadioSelect(),
        }
