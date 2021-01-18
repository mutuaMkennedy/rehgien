import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlencode
from markets import models as market_models
from location import models as location_models
from resource_center import models as resource_models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
from profiles import pro_profile_setup_forms as pro_setup_forms
from formtools.wizard.views import SessionWizardView

User = get_user_model()

def check_q_valid(param):
	return param !="" and param is not None

def homepage(request):
	return render(request,'rehgien_pro/rehgien_pro_homepage.html',{})

#pro onboarding wizard
FORMS = [
			("ProInfo", pro_setup_forms.ProInfo),
			("ProServices", pro_setup_forms.ProServices),
			("ProLocation", pro_setup_forms.ProLocation),
			("ProBusinessProfileImage", pro_setup_forms.ProBusinessProfileImage),
			("ProReviewers", pro_setup_forms.ProReviewers)
		 ]

TEMPLATES = {
			"ProInfo": "rehgien_pro/pro_onboarding/pro_info.html",
			"ProServices": "rehgien_pro/pro_onboarding/pro_services.html",
			"ProLocation": "rehgien_pro/pro_onboarding/pro_location.html",
			"ProBusinessProfileImage": "rehgien_pro/pro_onboarding/pro_business_profile_image.html",
			"ProReviewers": "rehgien_pro/pro_onboarding/pro_services.html"
			}

# @login_required(login_url='account_login')
class ProSetupWizardView(SessionWizardView):
	def get_template_names(self):
		print('next step ' + self.steps.current)
		return [TEMPLATES[self.steps.current]]
	file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_profile_photos'))
	def done(self, form_list, **kwargs):
		return render(self.request, 'done.html', {
			'form_data': [form.cleaned_data for form in form_list],
		})

@login_required(login_url='account_login')
def jobs_list(request):
	if request.user.user_type == 'PRO':
		location_target = str(request.GET.get("location_target",''))
		project_size = str(request.GET.get("project_size",''))
		project_duration = str(request.GET.get("project_duration",''))
		expertise_areas = str(request.GET.get("skill_areas",''))
		page = request.GET.get('page', '1')
		jobs = market_models.JobPost.objects.filter(active=True).order_by('-job_update_date')

		skill_areas = []
		for job in jobs:
			for skill in job.skill_areas:
				skill_areas.append(skill)
		skill_areas = list(set(skill_areas))

		town_names = []
		for town in location_models.KenyaTown.objects.all():
			town_names.append(town.town_name)

		if check_q_valid(location_target):
			jobs = jobs.filter(location__icontains = location_target)
		if check_q_valid(project_size):
			jobs = jobs.filter(project_size = project_size.upper())
		if check_q_valid(project_duration):
			jobs = jobs.filter(project_duration = project_duration)
		if check_q_valid(expertise_areas):
			jobs = jobs.filter(skill_areas__icontains = expertise_areas)

		paginator_jobs = Paginator(jobs, 20)
		jobs_p = paginator_jobs.get_page(page)

		search_params = {}
		search_params['location_target'] = location_target
		search_params['project_size'] = project_size
		search_params['project_duration'] = project_duration
		search_params['expertise_areas'] = expertise_areas
		search_params['page'] = page

		query_string = urlencode(search_params)

		context = {
			"jobs":jobs,
			"jobs_p":jobs_p,
			"skill_areas":skill_areas,
			"town_names":town_names,
			"search_params":search_params,
			"query_string":query_string
		}
		return render(request, 'rehgien_pro/job_list.html',context)
	else:
		messages.error(request,'Denied. This feature is availlable to pros only!')
		return redirect('rehgien_pro:rehgien_pro_homepage')

@login_required(login_url='account_login')
def job_detail(request, pk):
	if request.user.user_type == 'PRO':
		job = get_object_or_404(market_models.JobPost, id=pk)
		job_proposal = market_models.JobPostProposal.objects.filter(proposal_sender = request.user, job_post=job)
		if job.job_viewers.filter(pk=request.user.id).exists():
			pass
		else:
			job.job_viewers.add(request.user.id)

		context = {
				"job":job,
				"job_proposal":job_proposal
			}
		return render(request,  'rehgien_pro/job_post_detail.html', context)
	else:
		messages.error(request,'Denied. This feature is availlable to pros only!')
		return redirect('rehgien_pro:rehgien_pro_homepage')

def blog_posts(request):
	try:
		ImageTransformation = dict(
		format = "jpg",
		transformation = [
			dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
			 format="auto", dpr="auto", fl="progressive"),
				]
			)
		blog_article = request.GET.get('q_articles','')
		rq_blog_category = request.GET.get('blog_category','')

		all_blog_categories = resource_models.BlogCategory.objects.all()
		q_category = get_object_or_404(resource_models.BlogCategory, slug = rq_blog_category)
		posts = resource_models.BlogPost.objects.all()
		if check_q_valid(blog_article):
			posts = posts.filter(title__icontains = blog_article)
		if check_q_valid(rq_blog_category):
			posts = posts.filter(blog_category__slug = rq_blog_category)
		context = {
		"all_blog_categories":all_blog_categories,
		'posts':posts,
		"q_category":q_category,
		"ImageTransformation":ImageTransformation,
		"blog_article":blog_article,
		"rq_blog_category":rq_blog_category,
		'c':[1,2,3,4,5,6,7,8,9]
		}
		return render(request, 'rehgien_pro/blog_posts.html', context)
	except ObjectDoesNotExist as e:
		messages.error(request,'Resource you requested does not exists. Try again later!')
		return redirect('rehgien_pro:rehgien_pro_homepage')

def ajax_blog_post_autocomplete(request):
	if request.is_ajax():
		query = str(request.GET.get('term', ''))
		post = resource_models.BlogPost.objects.filter(title__icontains = query)
		results = []
		for post in post:
			results.append(post.title.capitalize())
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def blog_detail(request, slug):
	post = get_object_or_404(resource_models.BlogPost, slug = slug)
	context = {
	'post':post
	}
	return render(request, 'rehgien_pro/blog_post_detail.html', context)
