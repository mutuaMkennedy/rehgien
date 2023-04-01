from django import forms
from  . import models

class PartnerForm(forms.ModelForm):
    partner_program = forms.ModelChoiceField(queryset=models.PartnerProgram.objects, empty_label=None, widget=forms.RadioSelect())
    class Meta:
        model = models.RehgienPartner
        fields = [
            "partner_program","first_name","last_name",
            "email","company_name","company_website","phone_number","message"
        ]
        widgets ={
        "first_name":forms.TextInput(attrs={'placeholder':'First name'}),
        "last_name":forms.TextInput(attrs={'placeholder':'Last name'}),
        "email":forms.EmailInput(attrs={'placeholder':'abc@abc.com'}),
        "company_name":forms.TextInput(attrs={'placeholder':'abc'}),
        "company_website":forms.URLInput(attrs={'placeholder':'http://'}),
        "phone_number":forms.TextInput(attrs={'placeholder':'+254'})
        }
