from django.shortcuts import render,redirect
from django.contrib import messages
from .models import (
                    PropertyRequestLead,
                    ProffesionalRequestLead,
                    OtherServiceLead
                    )
from .forms import (
                    RequestPropertyForm,
                    RequestProffesionalForm,
                    OtherRequestForm
                    )
from django.contrib.auth import get_user_model

# referencing the custom user model
User = get_user_model()

def property_request_lead(request):
    if request.method =='POST':
        property_request_form = RequestPropertyForm(request.POST)
        # Authenticate form
        if property_request_form.is_valid():
            instance = property_request_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            messages.success(request, 'Your request has been posted Successfully!')
            return redirect('listings:homepage')
        else:
            messages.error(request,'Could not complete request. Try again later.')
    else:
        property_request_form = RequestPropertyForm()
    return render(request, 'markets/property_request_lead_form.html', {"form":property_request_form})

def proffesional_request_lead(request):
    if request.method =='POST':
        proffesional_request_form = RequestProffesionalForm(request.POST)
        # Authenticate form
        if proffesional_request_form.is_valid():
            instance = proffesional_request_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            messages.success(request, 'Your request has been posted Successfully!')
            return redirect('listings:homepage')
        else:
            messages.error(request,'Could not complete request. Try again later.')
    else:
        proffesional_request_form = RequestProffesionalForm()
    return render(request, 'markets/proffesional_request_lead_form.html', {"form":proffesional_request_form})

def other_request_lead(request):
    if request.method =='POST':
        other_request_form = OtherRequestForm(request.POST)
        # Authenticate form
        if other_request_form.is_valid():
            instance = other_request_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            messages.success(request, 'Your request has been posted Successfully!')
            return redirect('listings:homepage')
        else:
            messages.error(request,'Could not complete request. Try again later.')
    else:
        property_request_form = OtherRequestForm()
    return render(request, 'markets/other_request_lead_form.html', {"form":property_request_form})
