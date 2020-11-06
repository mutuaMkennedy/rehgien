from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import get_user_model

from . import models
from . import profile_edit_forms as forms


# referencing the custom user model
User = get_user_model()
weekdays = [{'day': 1},{'day': 2},{'day': 3},{'day': 4},{'day': 5},{'day': 6},{'day': 7}]

@login_required(login_url='account_login')
def agent_profile_editor_mode(request, pk):
    agent = get_object_or_404( models.AgentProfile, pk=pk )

    ag_top_client_formset = inlineformset_factory(
                models.AgentProfile, models.AgentTopClient, forms.AgentTopClientForm,
                min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                exclude=('created_by','created_at')
                )

    ag_business_hours_formset = inlineformset_factory(
                models.AgentProfile, models.AgentBusinessHours, forms.AgentBusinessHoursForm,
                min_num=1,max_num=14, extra=1, can_order=True, can_delete=True
                )

    user = request.user
    if user == agent.user:
        profile_image_form= forms.AgentProfileProfileImage(instance=user.agent_profile)
        page_info_form= forms.AgentProfilePageInfo(instance=user.agent_profile)
        about_form = forms.AgentProfileAbout(instance=user.agent_profile)
        services_form = forms.AgentProfileServices(instance=user.agent_profile)
        service_areas_form = forms.AgentProfileServiceAreas(instance=user.agent_profile)
        ag_client_formset = ag_top_client_formset(instance=agent)
        ag_hours_formset = ag_business_hours_formset(instance=agent)


        all_connections = models.TeammateConnection.objects.all()
        pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

        user_2 = agent.user
        user_1 = request.user
        agent_reviews = agent.agent_review.all()
        average_rating = agent_reviews.aggregate(Avg('rating'))
        reviews_count = agent_reviews.count()
        return render(request, 'profiles/editor_mode_files/agent_page_edit.html', {'agent':agent,
                    'agent_reviews':agent_reviews,'reviews_count':reviews_count, 'average_rating':average_rating,
                    "user_2":user_2,"user_1":user_1,'pro_teammates':pro_teammates,
                    "profile_image_form":profile_image_form,
                    "page_info_form":page_info_form,"about_form":about_form,
                    "services_form":services_form,"service_areas_form":service_areas_form,
                    "ag_client_formset":ag_client_formset,"ag_hours_formset":ag_hours_formset
                     })
    else:
        messages.error(request, 'Permission denied!')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def agent_profile_update(request, pk, slug):
    if request.is_ajax() and request.method == 'POST':
        agent_profile = get_object_or_404(models.AgentProfile, pk=pk )
        if slug == 'profile-picture':
            profile_image_form = forms.AgentProfileProfileImage(request.POST, request.FILES, instance=request.user.agent_profile)

            if profile_image_form.is_valid():
                if request.user == agent_profile.user:
                    profile_image_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }
                html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})




        elif slug == 'service-areas':
            service_areas_form = forms.AgentProfileServiceAreas(request.POST, instance=request.user.agent_profile)

            if service_areas_form.is_valid():
                if request.user == agent_profile.user:
                    service_areas_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }
                html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'our-services':
            services_form = forms.AgentProfileServices(request.POST, instance=request.user.agent_profile)

            if services_form.is_valid():
                if request.user == agent_profile.user:
                    services_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }
                html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'about-us':
            about_form = forms.AgentProfileAbout(request.POST, request.FILES, instance=request.user.agent_profile)
            if about_form.is_valid():
                if request.user == agent_profile.user:
                    about_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }
                html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'page-info':
            page_info_form = forms.AgentProfilePageInfo(request.POST, request.FILES, instance=request.user.agent_profile)
            ag_business_hours_formset = inlineformset_factory(
                        models.AgentProfile, models.AgentBusinessHours, forms.AgentBusinessHoursForm,
                        min_num=1,max_num=14, extra=1, can_order=True, can_delete=True
                        )
            ag_hours_formset = ag_business_hours_formset(request.POST, request.FILES, instance=agent_profile)

            if page_info_form.is_valid() and ag_hours_formset.is_valid():
                if request.user == agent_profile.user:
                    page_info_form.save()
                    ag_hours_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "ag_hours_formset":ag_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form,"ag_hours_formset":ag_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form,"ag_hours_formset":ag_hours_formset
                    }
                html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        elif slug == 'top-clients':
            ag_top_client_formset = inlineformset_factory(
                        models.AgentProfile, models.AgentTopClient, min_num=1,max_num=5, extra=0,
                        can_order=True,can_delete=True, exclude=('created_by','created_at')
                        )
            ag_client_formset = ag_top_client_formset(request.POST, request.FILES, instance=agent_profile)

            if ag_client_formset.is_valid():
                if request.user == agent_profile.user:
                    ag_client_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.AgentProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'ag_client_formset':ag_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'ag_client_formset':ag_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'ag_client_formset':ag_client_formset
                    }
                html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})

        else:
            messages.error(request, 'Invalid form requested. Changes no saved')
            return redirect('profiles:account')
    else:
        messages.error(request, 'Invalid request. Changes no saved')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def company_profile_editor_mode(request, pk):
    agent = get_object_or_404( models.CompanyProfile, pk=pk )
    co_top_client_formset = inlineformset_factory(
                models.CompanyProfile, models.CompanyTopClient, forms.CompanyTopClientForm,
                min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                exclude=('created_by','created_at')
                )

    co_business_hours_formset = inlineformset_factory(
                models.CompanyProfile, models.CompanyBusinessHours, forms.CompanyBusinessHoursForm,
                min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                )
    user = request.user
    if user == agent.user:
        profile_image_form= forms.CompanyProfileProfileImage(instance=user.company_profile)
        page_info_form= forms.CompanyProfilePageInfo(instance=user.company_profile)
        about_form = forms.CompanyProfileAbout(instance=user.company_profile)
        services_form = forms.CompanyProfileServices(instance=user.company_profile)
        service_areas_form = forms.CompanyProfileServiceAreas(instance=user.company_profile)

        co_client_formset = co_top_client_formset(instance=agent)
        co_hours_formset = co_business_hours_formset(instance=agent)

        all_connections = models.TeammateConnection.objects.all()
        pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

        user_2 = agent.user
        user_1 = request.user
        agent_reviews = agent.company_review.all()
        average_rating = agent_reviews.aggregate(Avg('rating'))
        reviews_count = agent_reviews.count()
        return render(request, 'profiles/editor_mode_files/company_page_edit.html', {'agent':agent,
                    'agent_reviews':agent_reviews,'reviews_count':reviews_count, 'average_rating':average_rating,
                    "user_2":user_2,"user_1":user_1,'pro_teammates':pro_teammates,
                    "profile_image_form":profile_image_form,
                    "page_info_form":page_info_form,"about_form":about_form,
                    "services_form":services_form,"service_areas_form":service_areas_form,
                    "co_client_formset":co_client_formset,"co_hours_formset":co_hours_formset
                     })
    else:
        messages.error(request, 'Permission denied!')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def company_profile_update(request, pk, slug):
    if request.is_ajax() and request.method == 'POST':
        agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )
        if slug == 'profile-picture':
            profile_image_form = forms.CompanyProfileProfileImage(request.POST, request.FILES, instance=request.user.company_profile)

            if profile_image_form.is_valid():
                if request.user == agent_profile.user:
                    profile_image_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }
                html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})




        elif slug == 'service-areas':
            service_areas_form = forms.CompanyProfileServiceAreas(request.POST, instance=request.user.company_profile)

            if service_areas_form.is_valid():
                if request.user == agent_profile.user:
                    service_areas_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }
                html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'our-services':
            services_form = forms.CompanyProfileServices(request.POST, instance=request.user.company_profile)

            if services_form.is_valid():
                if request.user == agent_profile.user:
                    services_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }
                html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'about-us':
            about_form = forms.CompanyProfileAbout(request.POST, request.FILES, instance=request.user.company_profile)
            if about_form.is_valid():
                if request.user == agent_profile.user:
                    about_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }
                html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'page-info':
            page_info_form = forms.CompanyProfilePageInfo(request.POST, request.FILES, instance=request.user.company_profile)
            co_business_hours_formset = inlineformset_factory(
                        models.CompanyProfile, models.CompanyBusinessHours, forms.CompanyBusinessHoursForm,
                        min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                        )
            co_hours_formset = co_business_hours_formset(request.POST, request.FILES, instance=agent_profile)

            if page_info_form.is_valid() and co_hours_formset.is_valid():
                if request.user == agent_profile.user:
                    page_info_form.save()
                    co_hours_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "co_hours_formset":co_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "co_hours_formset":co_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "co_hours_formset":co_hours_formset
                    }
                html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        elif slug == 'top-clients':
            co_top_client_formset = inlineformset_factory(
                        models.CompanyProfile, models.CompanyTopClient, forms.CompanyTopClientForm,
                        min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                        exclude=('created_by','created_at')
                        )
            co_client_formset = co_top_client_formset(request.POST, request.FILES, instance=agent_profile)

            if co_client_formset.is_valid():
                if request.user == agent_profile.user:
                    co_client_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.CompanyProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'co_client_formset':co_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'co_client_formset':co_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'co_client_formset':co_client_formset
                    }
                html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        else:
            messages.error(request, 'Invalid form requested. Changes no saved')
            return redirect('profiles:account')
    else:
        messages.error(request, 'Invalid request. Changes no saved')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def pm_profile_editor_mode(request, pk):
    agent = get_object_or_404( models.PropertyManagerProfile, pk=pk )
    pm_top_client_formset = inlineformset_factory(
                models.PropertyManagerProfile, models.PropertyManagerTopClient, forms.PropertyManagerTopClientForm,
                min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                exclude=('created_by','created_at')
                )

    pm_business_hours_formset = inlineformset_factory(
                models.PropertyManagerProfile, models.PropertyManagerBusinessHours, forms.PropertyManagerBusinessHoursForm,
                min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                )

    user = request.user
    if user == agent.user:
        profile_image_form= forms.PmProfileProfileImage(instance=user.pm_profile)
        page_info_form= forms.PmProfilePageInfo(instance=user.pm_profile)
        about_form = forms.PmProfileAbout(instance=user.pm_profile)
        # services_form = forms.PmProfileServices(instance=user.pm_profile)
        service_areas_form = forms.PmProfileServiceAreas(instance=user.pm_profile)

        pm_client_formset = pm_top_client_formset(instance=agent)
        pm_hours_formset = pm_business_hours_formset(instance=agent)

        all_connections = models.TeammateConnection.objects.all()
        pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

        user_2 = agent.user
        user_1 = request.user
        agent_reviews = agent.pm_review.all()
        average_rating = agent_reviews.aggregate(Avg('rating'))
        reviews_count = agent_reviews.count()
        return render(request, 'profiles/editor_mode_files/pm_page_edit.html', {'agent':agent,
                    'agent_reviews':agent_reviews,'reviews_count':reviews_count, 'average_rating':average_rating,
                    "user_2":user_2,"user_1":user_1,'pro_teammates':pro_teammates,
                    "profile_image_form":profile_image_form,
                    "page_info_form":page_info_form,"about_form":about_form,
                    # "services_form":services_form,
                    "service_areas_form":service_areas_form, "pm_client_formset":pm_client_formset,
                    "pm_hours_formset":pm_hours_formset
                     })
    else:
        messages.error(request, 'Permission denied!')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def pm_profile_update(request, pk, slug):
    if request.is_ajax() and request.method == 'POST':
        agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )
        if slug == 'profile-picture':
            profile_image_form = forms.PmProfileProfileImage(request.POST, request.FILES, instance=request.user.pm_profile)

            if profile_image_form.is_valid():
                if request.user == agent_profile.user:
                    profile_image_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }
                html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})




        elif slug == 'service-areas':
            service_areas_form = forms.PmProfileServiceAreas(request.POST, instance=request.user.pm_profile)

            if service_areas_form.is_valid():
                if request.user == agent_profile.user:
                    service_areas_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }
                html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        # elif slug == 'our-services':
        #     services_form = forms.PmProfileServices(request.POST, instance=request.user.pm_profile)
        #
        #     if services_form.is_valid():
        #         if request.user == agent_profile.user:
        #             services_form.save()
        #
        #             #we request an updated instance of the model
        #             agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )
        #
        #             message = 'Changes saved successfully!'
        #             context = {
        #             'message':message,'agent':agent_profile,'services_form':services_form
        #             }
        #
        #             html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
        #             return JsonResponse({'page_section':html ,'message':message})
        #         else:
        #             message = 'Permission denied. Changes not saved'
        #             context = {
        #             'message':message,'agent':agent_profile,'services_form':services_form
        #             }
        #
        #             html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
        #             return JsonResponse({'page_section':html ,'message':message})
        #
        #     else:
        #         message = 'Invalid form submission!'
        #         context = {
        #             'message':message,'agent':agent_profile,'services_form':services_form
        #             }
        #         html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
        #         return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'about-us':
            about_form = forms.PmProfileAbout(request.POST, request.FILES, instance=request.user.pm_profile)
            if about_form.is_valid():
                if request.user == agent_profile.user:
                    about_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }
                html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'page-info':
            page_info_form = forms.PmProfilePageInfo(request.POST, request.FILES, instance=request.user.pm_profile)
            pm_business_hours_formset = inlineformset_factory(
                        models.PropertyManagerProfile, models.PropertyManagerBusinessHours, forms.PropertyManagerBusinessHoursForm,
                        min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                        )
            pm_hours_formset = pm_business_hours_formset(request.POST, request.FILES, instance=agent_profile)
            if page_info_form.is_valid() and pm_hours_formset.is_valid():
                if request.user == agent_profile.user:
                    page_info_form.save()
                    pm_hours_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "pm_hours_formset":pm_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form,"pm_hours_formset":pm_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "pm_hours_formset":pm_hours_formset
                    }
                html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        elif slug == 'top-clients':
            pm_top_client_formset = inlineformset_factory(
                        models.PropertyManagerProfile, models.PropertyManagerTopClient, forms.PropertyManagerTopClientForm,
                        min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                        exclude=('created_by','created_at')
                        )
            pm_client_formset = pm_top_client_formset(request.POST, request.FILES, instance=agent_profile)

            if pm_client_formset.is_valid():
                if request.user == agent_profile.user:
                    pm_client_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.PropertyManagerProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'pm_client_formset':pm_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'pm_client_formset':pm_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'pm_client_formset':pm_client_formset
                    }
                html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        else:
            messages.error(request, 'Invalid form requested. Changes no saved')
            return redirect('profiles:account')
    else:
        messages.error(request, 'Invalid request. Changes no saved')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def ds_profile_editor_mode(request, pk):
    agent = get_object_or_404( models.DesignAndServiceProProfile, pk=pk )
    ds_top_client_formset = inlineformset_factory(
                models.DesignAndServiceProProfile, models.DSTopClient, forms.DSTopClientForm,
                min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                exclude=('created_by','created_at')
                )

    ds_business_hours_formset = inlineformset_factory(
                models.DesignAndServiceProProfile, models.DSBusinessHours, forms.DSBusinessHoursForm,
                min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                )

    user = request.user
    if user == agent.user:
        profile_image_form= forms.DSProfileProfileImage(instance=user.DService_profile)
        page_info_form= forms.DSProfilePageInfo(instance=user.DService_profile)
        about_form = forms.DSProfileAbout(instance=user.DService_profile)
        services_form = forms.DSProfileServices(instance=user.DService_profile)
        service_areas_form = forms.DSProfileServiceAreas(instance=user.DService_profile)

        ds_client_formset = ds_top_client_formset(instance=agent)
        ds_hours_formset = ds_business_hours_formset(instance=agent)


        all_connections = models.TeammateConnection.objects.all()
        pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

        user_2 = agent.user
        user_1 = request.user
        agent_reviews = agent.DService_review.all()
        average_rating = agent_reviews.aggregate(Avg('rating'))
        reviews_count = agent_reviews.count()
        return render(request, 'profiles/editor_mode_files/ds_page_edit.html', {'agent':agent,
                    'agent_reviews':agent_reviews,'reviews_count':reviews_count, 'average_rating':average_rating,
                    "user_2":user_2,"user_1":user_1,'pro_teammates':pro_teammates,
                    "profile_image_form":profile_image_form,
                    "page_info_form":page_info_form,"about_form":about_form,
                    "services_form":services_form,"service_areas_form":service_areas_form,
                    "ds_client_formset":ds_client_formset, "ds_hours_formset":ds_hours_formset
                     })
    else:
        messages.error(request, 'Permission denied!')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def ds_profile_update(request, pk, slug):
    if request.is_ajax() and request.method == 'POST':
        agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )
        if slug == 'profile-picture':
            profile_image_form = forms.DSProfileProfileImage(request.POST, request.FILES, instance=request.user.DService_profile)

            if profile_image_form.is_valid():
                if request.user == agent_profile.user:
                    profile_image_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }

                    html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'profile_image_form':profile_image_form
                    }
                html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})




        elif slug == 'service-areas':
            service_areas_form = forms.DSProfileServiceAreas(request.POST, instance=request.user.DService_profile)

            if service_areas_form.is_valid():
                if request.user == agent_profile.user:
                    service_areas_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }

                    html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'service_areas_form':service_areas_form
                    }
                html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'our-services':
            services_form = forms.DSProfileServices(request.POST, instance=request.user.DService_profile)

            if services_form.is_valid():
                if request.user == agent_profile.user:
                    services_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }

                    html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'services_form':services_form
                    }
                html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'about-us':
            about_form = forms.DSProfileAbout(request.POST, request.FILES, instance=request.user.DService_profile)
            if about_form.is_valid():
                if request.user == agent_profile.user:
                    about_form.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }

                    html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'about_form':about_form
                    }
                html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
                return JsonResponse({'page_section':html ,'message':message})
        elif slug == 'page-info':
            page_info_form = forms.DSProfilePageInfo(request.POST, request.FILES, instance=request.user.DService_profile)
            ds_business_hours_formset = inlineformset_factory(
                        models.DesignAndServiceProProfile, models.DSBusinessHours, forms.DSBusinessHoursForm,
                        min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
                        )
            ds_hours_formset = ds_business_hours_formset(request.POST, request.FILES, instance=agent_profile)

            if page_info_form.is_valid() and ds_hours_formset.is_valid():
                if request.user == agent_profile.user:
                    page_info_form.save()
                    ds_hours_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "ds_hours_formset":ds_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "ds_hours_formset":ds_hours_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'page_info_form':page_info_form, "ds_hours_formset":ds_hours_formset
                    }
                html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        elif slug == 'top-clients':
            ds_top_client_formset = inlineformset_factory(
                        models.DesignAndServiceProProfile, models.DSTopClient, forms.DSTopClientForm,
                        min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
                        exclude=('created_by','created_at')
                        )
            ds_client_formset = ds_top_client_formset(request.POST, request.FILES, instance=agent_profile)

            if ds_client_formset.is_valid():
                if request.user == agent_profile.user:
                    ds_client_formset.save()

                    #we request an updated instance of the model
                    agent_profile = get_object_or_404(models.DesignAndServiceProProfile, pk=pk )

                    message = 'Changes saved successfully!'
                    context = {
                    'message':message,'agent':agent_profile,'ds_client_formset':ds_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})
                else:
                    message = 'Permission denied. Changes not saved'
                    context = {
                    'message':message,'agent':agent_profile,'ds_client_formset':ds_client_formset
                    }

                    html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                    return JsonResponse({'page_section':html ,'message':message})

            else:
                message = 'Invalid form submission!'
                context = {
                    'message':message,'agent':agent_profile,'ds_client_formset':ds_client_formset
                    }
                html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
                return JsonResponse({'page_info_section':html ,'message':message})
        else:
            messages.error(request, 'Invalid form requested. Changes no saved')
            return redirect('profiles:account')
    else:
        messages.error(request, 'Invalid request. Changes no saved')
        return redirect('profiles:account')
