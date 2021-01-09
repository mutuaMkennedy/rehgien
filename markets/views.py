from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from . import models
from . import forms
from profiles import models as profiles_models
from location import models as location_models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.template.loader import render_to_string
with connection.cursor() as cursor:
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json

from django.core.exceptions import ObjectDoesNotExist

# referencing the custom user model
User = get_user_model()

def check_q_valid(param):
	return param !="" and param is not None

def match_pros(title):
    # pros = profiles_models.BusinessProfile.objects.annotate(
    #         similarity=TrigramSimilarity('professional_services', title),
    #         ).filter(similarity__gt=0)
    tag_array = title.split(' ')
    for tag in tag_array:
        pros = profiles_models.BusinessProfile.objects.filter(
                professional_services__service_name__icontains=tag,
                )
        return pros

def ajax_search_pros(request):
    if request.method == 'GET' and request.is_ajax():
        q = str(request.GET.get('job_title'))
        pros = match_pros(q)
        pro_services = []
        for  pro in pros:
            for service in pro.professional_services.all():
                pro_services.append(service.service_name.lower())
        pro_services = list(set(pro_services))
        split_text = q.split(' ')
        if len(split_text) < 3: # incase user bypasses the js word check
            message = 'fail'
            msg_body = 'That title is a bit short. Add a more descriptive title to increase the chances of finding a match.'
            return JsonResponse({'message':message,'msg_body':msg_body})
        elif len(pros) == 0:
            message = 'fail'
            msg_body = 'That title is a bit narrow. Add a more descriptive title to increase the chances of finding a match.'
            return JsonResponse({'message':message,'msg_body':msg_body})
        else:
            message = 'pass'
            string = '+ professionals' if pros.count() > 10 else ' professionals.'
            msg_body = 'Great! We found ' + str(pros.count()) + string
            return JsonResponse({'message':message,'msg_body':msg_body,'pro_services':pro_services})
    else:
        messages.error(request,'Invalid request. Try again later')
        return redirect('markets:job_post_create')

def ajax_search_service(request):
    if request.is_ajax():
        query = str(request.GET.get('term', ''))
        results = []
        for services in profiles_models.ProfessionalService.objects.filter(service_name__icontains = query):
            results.append(services.service_name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def job_post_home(request):
    return render(request,'markets/job_post_homepage.html',{})

@login_required(login_url='account_login')
def job_post_detail(request,pk):
    job_post = get_object_or_404(models.JobPost, id=pk)
    if request.user == job_post.job_poster:
        context = {
            "job":job_post
            }
        return render(request,'markets/job_post_detail.html',context)
    else:
        messages.error('Permission denied!')
        return redirect('profiles:account')

@login_required(login_url='account_login')
def job_post_create(request):
    if request.method =='POST':
        job_post_form = forms.JobPostForm(request.POST)
        # Authenticate form
        if job_post_form.is_valid():
            instance = job_post_form.save(commit=False)
            instance.job_poster = request.user
            instance.active = True
            instance.save()

            messages.success(request, 'Your request has been posted Successfully!')
            return redirect('profiles:account')
        else:
            messages.error(request,'Invalid form. Check your fields and try.')
    else:
        town_names = []
        for town in location_models.KenyaTown.objects.all():
            town_names.append(town.town_name)
        job_post_form = forms.JobPostForm()
    return render(request, 'markets/job_post_form.html', {"job_post_form":job_post_form,"town_names":town_names})

@login_required(login_url='account_login')
def job_post_update(request,pk):
    job_post = get_object_or_404(models.JobPost, pk=pk)
    if request.user == job_post.job_poster:
        if request.method =='POST':
            job_post_form = forms.JobPostForm(request.POST, instance=job_post)
            if job_post_form.is_valid():
                job_post_form.save()

                messages.success(request, 'Your request has been updated Successfully!')
                return redirect('profiles:account')
            else:
                messages.error(request,'Could not complete request. Try again later.')
        else:
            job_post_form = forms.JobPostForm(instance=job_post)
    else:
        messages.error(request,'Permission denied')
    return render(request, 'markets/job_post_update_form.html', {"job_post_form":job_post_form,'job_post':job_post})

@login_required(login_url='account_login')
def job_post_deactivate(request,pk):
    job_post = get_object_or_404(models.JobPost, pk=pk)
    if request.user == job_post.job_poster:
        if request.method =='POST':
            job_post.active = False
            job_post.save()
            messages.success(request,"Job successfully deactivated")
            return redirect('profiles:account')
        else:
            messages.error(request,'Request not allowed!')
            return redirect('profiles:account')
    else:
        messages.error(request,"Permission denied")
        return redirect('profiles:account')

@login_required(login_url='account_login')
def submit_proposal(request, pk):
    id = pk
    if request.method == 'POST':
        try:
            reply_message = str(request.POST.get('post_reply',''))
            job = get_object_or_404(models.JobPost, pk=id)
            if check_q_valid(reply_message):
                message = ''
                success = ''
                if job.job_post_proposal.filter(proposal_sender = request.user).exists():
                    message = "Message not sent. You have already replied to this jobpost!"
                    success = 'False'
                else:
                    proposal = models.JobPostProposal.objects.create(
                                job_post = job,
                                message = reply_message,
                                proposal_sender = request.user
                                )
                    proposal.save()
                    message = "Message sent successfully."
                    success = 'True'

                job_proposal = models.JobPostProposal.objects.filter(proposal_sender = request.user, job_post=job)
                context = {
                        "job_proposal":job_proposal,
                        "message":message,
                        "success":success
                    }
                if request.is_ajax():
                    replied_section = render_to_string('rehgien_pro/replied_to_job_post.html', context, request=request)
                    return JsonResponse({'replied_section':replied_section, 'message':message,'success':success})
                else:
                    messages.success(request,'Message sent successfully.')
                    return redirect('rehgien_pro:job_detail', pk=id)
            else:
                message = "Message not sent! Make sure the message field is not empty."
                success = 'False'
                if request.is_ajax():
                    return JsonResponse({'message':message,
                        'success':success})
                else:
                    messages.success(request,'Message sent successfully.')
                    return redirect('rehgien_pro:job_detail', pk=id)

        except ObjectDoesNotExist as e:
            message = 'Ooops! Something went wrong. Try again later!'
            success = 'False'
            if request.is_ajax():
                return JsonResponse({'message':message,
                    'success':success})
    else:
        return redirect ('rehgien_pro:job_detail', pk=id)
