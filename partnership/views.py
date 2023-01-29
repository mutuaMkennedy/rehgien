from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from . import forms


def partner_program_home(request):
    program = models.PartnerProgram.objects.all().exclude(title = 'Other')
    if request.method == 'POST':
        partnership_form = forms.PartnerForm(request.POST, request.FILES)
        if partnership_form.is_valid():
            partnership_form.save()
            messages.success(request,"Thanks for applying we'll be in touch!")
            return redirect("partnership:partner_program_home")
        else:
            messages.error(request,"Invalid submission. Check the form for field errors.")
    else:
        partnership_form = forms.PartnerForm()
    context = {
        "program":program,
        "partnership_form":partnership_form
    }
    return render(request, 'partnership/partnership_homepage.html', context)
