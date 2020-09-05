from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import (
                    PropertyRequestLead,
                    ProffesionalRequestLead,
                    OtherServiceLead,
                    AgentLeadRequest,
                    AgentPropertyRequest
                    )
from .forms import (
                    RequestPropertyForm,
                    RequestProffesionalForm,
                    OtherRequestForm,
                    AgentLeadRequestForm,
                    AgentPropertyRequestForm
                    )
from django.contrib.auth import get_user_model

# referencing the custom user model
User = get_user_model()

# List views
def request_list(request):
    property_requests = PropertyRequestLead.objects.all().filter(active=True).filter(owner=request.user)
    proffesional_requests = ProffesionalRequestLead.objects.all().filter(active=True).filter(owner=request.user)
    other_requests = OtherServiceLead.objects.all().filter(active=True).filter(owner=request.user)
    ag_lead_requests = AgentLeadRequest.objects.all().filter(active=True).filter(owner=request.user)
    ag_property_requests = AgentPropertyRequest.objects.all().filter(active=True).filter(owner=request.user)
    return render(request, 'profiles/templates/profiles/user_profile.html', {
    "property_requests":property_requests,"proffesional_requests":proffesional_requests,
    "other_requests":other_requests,"ag_lead_requests":ag_lead_requests,"ag_property_requests":ag_property_requests
    })

# Create views
@login_required(login_url='account_login')
def property_request_lead(request):
    if request.method =='POST':
        if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
            if request.user.user_type =='NormalUser':
                if request.user.n_user_profile.profile_image:
                    profile_image = request.user.n_user_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            if request.user.user_type =='Design&servicePro':
                if request.DService_profile.profile_image:
                    profile_image = request.DService_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            property_request_form = RequestPropertyForm(request.POST)
            # Authenticate form
            if property_request_form.is_valid():
                instance = property_request_form.save(commit=False)
                instance.owner = request.user
                instance.profile_image = request.build_absolute_uri(profile_image)
                instance.save()

                messages.success(request, 'Your request has been posted Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
            return redirect('profiles:account')
    else:
        property_request_form = RequestPropertyForm()
    return render(request, 'markets/property_request_lead_form.html', {"form":property_request_form})

@login_required(login_url='account_login')
def proffesional_request_lead(request):
    if request.method =='POST':
        if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
            if request.user.user_type =='NormalUser':
                if request.user.n_user_profile.profile_image:
                    profile_image = request.user.n_user_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            if request.user.user_type =='Design&servicePro':
                if request.DService_profile.profile_image:
                    profile_image = request.DService_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            proffesional_request_form = RequestProffesionalForm(request.POST)
            # Authenticate form
            if proffesional_request_form.is_valid():
                instance = proffesional_request_form.save(commit=False)
                instance.owner = request.user
                instance.profile_image = request.build_absolute_uri(profile_image)
                instance.save()

                messages.success(request, 'Your request has been posted Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
            return redirect('profiles:account')
    else:
        proffesional_request_form = RequestProffesionalForm()
    return render(request, 'markets/proffesional_request_lead_form.html', {"form":proffesional_request_form})

@login_required(login_url='account_login')
def other_request_lead(request):
    if request.method =='POST':
        if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
            if request.user.user_type =='NormalUser':
                if request.user.n_user_profile.profile_image:
                    profile_image = request.user.n_user_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            if request.user.user_type =='Design&servicePro':
                if request.DService_profile.profile_image:
                    profile_image = request.DService_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            other_request_form = OtherRequestForm(request.POST)
            # Authenticate form
            if other_request_form.is_valid():
                instance = other_request_form.save(commit=False)
                instance.owner = request.user
                instance.profile_image = request.build_absolute_uri(profile_image)
                instance.save()

                messages.success(request, 'Your request has been posted Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
            return redirect('profiles:account')
    else:
        property_request_form = OtherRequestForm()
    return render(request, 'markets/other_request_lead_form.html', {"form":property_request_form})

@login_required(login_url='account_login')
def agent_lead_request(request):
    if request.method =='POST':
        if request.user.user_type =='Agent' or request.user.user_type =='PropertyManager':
            if request.user.user_type =='Agent':
                if request.user.agent_profile.profile_image:
                    profile_image = request.user.agent_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            if request.user.user_type =='PropertyManager':
                if request.user.pm_profile.profile_image:
                    profile_image = request.user.pm_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            agent_lead_request_form = AgentLeadRequestForm(request.POST)
            # Authenticate form
            if agent_lead_request_form.is_valid():
                instance = agent_lead_request_form.save(commit=False)
                instance.owner = request.user
                instance.profile_image = request.build_absolute_uri(profile_image)
                instance.save()

                messages.success(request, 'Your request has been posted Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            messages.error(request,'Restricted. This service is for Real Estate Pros only.')
            return redirect('profiles:account')
    else:
        agent_lead_request_form = AgentLeadRequestForm()
    return render(request, 'markets/agent_lead_request_form.html', {"form":agent_lead_request_form})

@login_required(login_url='account_login')
def agent_property_request(request):
    if request.method =='POST':
        if request.user.user_type =='Agent' or request.user.user_type =='PropertyManager':
            if request.user.user_type =='Agent':
                if request.user.agent_profile.profile_image:
                    profile_image = request.user.agent_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            if request.user.user_type =='PropertyManager':
                if request.user.pm_profile.profile_image:
                    profile_image = request.user.pm_profile.profile_image.url
                else:
                    profile_image = '/static/img/avatar.png'
            ag_prop_request_form = AgentPropertyRequestForm(request.POST)
            # Authenticate form
            if ag_prop_request_form.is_valid():
                instance = ag_prop_request_form.save(commit=False)
                instance.owner = request.user
                instance.save()

                messages.success(request, 'Your request has been posted Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            messages.error(request,'Restricted. This service is for Real Estate Pros only.')
            return redirect('profiles:account')
    else:
        ag_prop_request_form = AgentPropertyRequestForm()
    return render(request, 'markets/agent_property_request_form.html', {"form":ag_prop_request_form})

# Update views

@login_required(login_url='account_login')
def property_request_lead_update(request,pk):
    property_request = get_object_or_404(PropertyRequestLead, pk=pk)
    if request.user == property_request.owner:
        if request.method =='POST':
            if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
                if request.user.user_type =='NormalUser':
                    if request.user.n_user_profile.profile_image:
                        profile_image = request.user.n_user_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                if request.user.user_type =='Design&servicePro':
                    if request.DService_profile.profile_image:
                        profile_image = request.DService_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                property_request_form = RequestPropertyForm(request.POST, instance=property_request)
                # Authenticate form
                if property_request_form.is_valid():
                    instance = property_request_form.save(commit=False)
                    instance.owner = request.user
                    instance.profile_image = request.build_absolute_uri(profile_image)
                    instance.save()

                    messages.success(request, 'Your request has been updated Successfully!')
                    return redirect('profiles:account')
                else:
                    messages.error(request,'Could not complete request. Try again later.')
            else:
                messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
                return redirect('profiles:account')
        else:
            property_request_form = RequestPropertyForm(instance=property_request)
    else:
        raise PermissionDenied
    return render(request, 'markets/property_request_lead_update_form.html', {"form":property_request_form,'request':property_request})

@login_required(login_url='account_login')
def proffesional_request_lead_update(request,pk):
    pro_request = get_object_or_404(ProffesionalRequestLead, pk=pk)
    if request.user == pro_request.owner:
        if request.method =='POST':
            if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
                if request.user.user_type =='NormalUser':
                    if request.user.n_user_profile.profile_image:
                        profile_image = request.user.n_user_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                if request.user.user_type =='Design&servicePro':
                    if request.DService_profile.profile_image:
                        profile_image = request.DService_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                pro_request_form = RequestProffesionalForm(request.POST, instance=pro_request)
                # Authenticate form
                if pro_request_form.is_valid():
                    instance = pro_request_form.save(commit=False)
                    instance.owner = request.user
                    instance.profile_image = request.build_absolute_uri(profile_image)
                    instance.save()

                    messages.success(request, 'Your request has been updated Successfully!')
                    return redirect('profiles:account')
                else:
                    messages.error(request,'Could not complete request. Try again later.')
            else:
                messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
                return redirect('profiles:account')
        else:
            pro_request_form = RequestProffesionalForm(instance=pro_request)
    else:
        raise PermissionDenied
    return render(request, 'markets/proffesional_request_lead_update_form.html', {"form":pro_request_form,'request':pro_request})

@login_required(login_url='account_login')
def other_request_lead_update(request,pk):
    o_request = get_object_or_404(OtherServiceLead, pk=pk)
    if request.user == o_request.owner:
        if request.method =='POST':
            if request.user.user_type =='NormalUser' or request.user.user_type =='Design&servicePro':
                if request.user.user_type =='NormalUser':
                    if request.user.n_user_profile.profile_image:
                        profile_image = request.user.n_user_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                if request.user.user_type =='Design&servicePro':
                    if request.DService_profile.profile_image:
                        profile_image = request.DService_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                o_request_form = OtherRequestForm(request.POST, instance=o_request)
                # Authenticate form
                if o_request_form.is_valid():
                    instance = o_request_form.save(commit=False)
                    instance.owner = request.user
                    instance.profile_image = request.build_absolute_uri(profile_image)
                    instance.save()

                    messages.success(request, 'Your request has been updated Successfully!')
                    return redirect('profiles:account')
                else:
                    messages.error(request,'Could not complete request. Try again later.')
            else:
                messages.error(request,'Restricted. This service is not availlable to Real Estate Pros.')
                return redirect('profiles:account')
        else:
            o_request_form = OtherRequestForm(instance=o_request)
    else:
        raise PermissionDenied
    return render(request, 'markets/other_request_lead_update_form.html', {"form":o_request_form,'request':o_request})

@login_required(login_url='account_login')
def agent_lead_request_update(request,pk):
    agent_lead_request = get_object_or_404(AgentLeadRequest, pk=pk)
    if request.user == agent_lead_request.owner:
        if request.method =='POST':
            if request.user.user_type =='Agent' or request.user.user_type =='PropertyManager':
                if request.user.user_type =='Agent':
                    if request.user.agent_profile.profile_image:
                        profile_image = request.user.agent_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                if request.user.user_type =='PropertyManager':
                    if request.user.pm_profile.profile_image:
                        profile_image = request.user.pm_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                agent_lead_request_form = AgentLeadRequestForm(request.POST, instance=agent_lead_request)
                # Authenticate form
                if agent_lead_request_form.is_valid():
                    instance = agent_lead_request_form.save(commit=False)
                    instance.owner = request.user
                    instance.profile_image = request.build_absolute_uri(profile_image)
                    instance.save()

                    messages.success(request, 'Your request has been updated Successfully!')
                    return redirect('profiles:account')
                else:
                    messages.error(request,'Could not complete request. Try again later.')
            else:
                messages.error(request,'Restricted. This service is for Real Estate Pros only.')
                return redirect('profiles:account')
        else:
            agent_lead_request_form = AgentLeadRequestForm(instance=agent_lead_request)
    else:
        raise PermissionDenied
    return render(request, 'markets/agent_lead_request_update_form.html', {"form":agent_lead_request_form,'request':agent_lead_request})

@login_required(login_url='account_login')
def agent_property_request_update(request,pk):
    agent_prop_request = get_object_or_404(AgentPropertyRequest, pk=pk)
    if request.user == agent_prop_request.owner:
        if request.method =='POST':
            if request.user.user_type =='Agent' or request.user.user_type =='PropertyManager':
                if request.user.user_type =='Agent':
                    if request.user.agent_profile.profile_image:
                        profile_image = request.user.agent_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                if request.user.user_type =='PropertyManager':
                    if request.user.pm_profile.profile_image:
                        profile_image = request.user.pm_profile.profile_image.url
                    else:
                        profile_image = '/static/img/avatar.png'
                agent_prop_request_form = AgentPropertyRequestForm(request.POST, instance=agent_prop_request)
                # Authenticate form
                if agent_prop_request_form.is_valid():
                    instance = agent_prop_request_form.save(commit=False)
                    instance.owner = request.user
                    instance.profile_image = request.build_absolute_uri(profile_image)
                    instance.save()

                    messages.success(request, 'Your request has been updated Successfully!')
                    return redirect('profiles:account')
                else:
                    messages.error(request,'Could not complete request. Try again later.')
            else:
                messages.error(request,'Restricted. This service is for Real Estate Pros only.')
                return redirect('profiles:account')
        else:
            agent_prop_request_form = AgentPropertyRequestForm(instance=agent_prop_request)
    else:
        raise PermissionDenied
    return render(request, 'markets/agent_property_request_update_form.html', {"form":agent_prop_request_form,'request':agent_prop_request})

# Deactivate views
@login_required(login_url='account_login')
def property_request_lead_deactivate(request,pk):
    property_request = get_object_or_404(PropertyRequestLead, pk=pk)
    if request.user == property_request.owner:
        if request.method =='POST':
            property_request.active = False
            property_request.save()
            messages.success(request,"Request Successfully Deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"You don't have the necessary permissions to perform that action.")
        return redirect('profiles:account')

@login_required(login_url='account_login')
def proffesional_request_lead_deactivate(request,pk):
    pro_request = get_object_or_404(ProffesionalRequestLead, pk=pk)
    if request.user == pro_request.owner:
        if request.method =='POST':
            pro_request.active = False
            pro_request.save()
            messages.success(request,"Request Successfully Deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"You don't have the necessary permissions to perform that action.")
        return redirect('profiles:account')

@login_required(login_url='account_login')
def other_request_lead_deactivate(request,pk):
    o_request = get_object_or_404(OtherServiceLead, pk=pk)
    if request.user == o_request.owner:
        if request.method =='POST':
            o_request.update.active = False
            o_request.save()
            messages.success(request,"Request Successfully Deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"You don't have the necessary permissions to perform that action.")
        return redirect('profiles:account')

@login_required(login_url='account_login')
def agent_lead_request_deactivate(request,pk):
    agent_lead_request = get_object_or_404(AgentLeadRequest, pk=pk)
    if request.user == agent_lead_request.owner:
        if request.method =='POST':
            agent_lead_request.active = False
            agent_lead_request.save()
            messages.success(request,"Request Successfully Deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"You don't have the necessary permissions to perform that action.")
        return redirect('profiles:account')

@login_required(login_url='account_login')
def agent_property_request_deactivate(request,pk):
    agent_prop_request = get_object_or_404(AgentPropertyRequest, pk=pk)
    if request.user == agent_prop_request.owner:
        if request.method =='POST':
            agent_prop_request.active = False
            agent_prop_request.save()
            messages.success(request,"Request Successfully Deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"You don't have the necessary permissions to perform that action.")
        return redirect('profiles:account')
