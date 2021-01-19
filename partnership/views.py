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
    partnership_form = forms.PartnerForm()
    context = {
        "program":program,
        "partnership_form":partnership_form
    }

    return render(request, 'partnership/partnership_homepage.html', context)

def partnership_form(request):
    name = request.POST.get('name', '')
    business_category = request.POST.get('phone_number', '')
    subject = 'Request to partner'
    sender_message = 'Helloi i am interested in partnering'
    email = request.POST.get('message', '')
    phone_number = request.POST.get('from_email', '')
    if request.method == 'POST':
        if name and business_category and  sender_message and email and phone_number:
            try:
                plainMessage =  sender_message  + '\nSubmited user data' + '\n Name: ' + name + \
                                '\n Phone number: ' + phone_number  + '\n Email: ' + email

                send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
            except BadHeaderError:
                messages.error(request, 'Something went wrong! Could not complete request. Try again later')
                return redirect(request.get_absolute_url())
        else:
            messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
            return redirect(request.get_absolute_url())
    else:
        partnerhip_form = forms.PartnerForm()
        context = {
        "partnerhip_form":partnerhip_form
        }
        return render(request, 'partnership/partnership_form.html',context)
