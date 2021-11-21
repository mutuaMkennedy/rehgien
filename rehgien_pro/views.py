import os
import io
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlencode
from . import forms
from markets import models as market_models
from location import models as location_models
from profiles import models as profiles_models
from listings import models as listings_models
from resource_center import models as resource_models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
from profiles import pro_profile_setup_forms as pro_setup_forms
from formtools.wizard.views import SessionWizardView
from django.utils.functional import cached_property
from django.contrib.sites.models import Site


User = get_user_model()

#helper functions
def check_q_valid(param):
	return param !="" and param is not None

def milestones_complete(user_pk):
	user = User.objects.get(pk=int(user_pk))
	milestones = { 'account_created':False, 'business_profile_photo':False,
	 'professional_services':False, 'business_description':False,
	 'work_projects':False, 'reviews':False
	}

	complete = 0
	if user.user_type == 'PRO':
		milestones['account_created'] = True
		complete +=1
	if user.pro_business_profile.business_profile_image:
		milestones['business_profile_photo'] = True
		complete +=1
	if user.pro_business_profile.professional_services:
		milestones['professional_services'] = True
		complete +=1
	if user.pro_business_profile.about:
		milestones['business_description'] = True
		complete +=1
	if user.profiles_portfolioitem_createdby_related.count() > 2 :
		milestones['work_projects'] = True
		complete +=1
	if user.pro_business_profile.pro_business_review.count() > 2 :
		milestones['reviews'] = True
		complete +=1
	results = {
	"milestones":milestones,
	"complete": complete
	}
	return results

#pro Dash board views

@login_required(login_url='app_accounts:user_login')
def dashboard_home(request):
	if request.user.user_type == 'PRO':
		results = milestones_complete(request.user.pk)
		pro_page = profiles_models.BusinessProfile.objects.get(user=request.user)
		blog_posts = resource_models.BlogPost.objects.all().order_by('-publishdate')[:10]
		context = {
		"results":results,
		"pro_page":pro_page,
		"blog_posts":blog_posts
		}
		return render(request, 'rehgien_pro/dashboard/homepage.html', context)
	else:
		messages.error(request,'Denied. Upgrade to a Pro to continue.')
		return redirect('rehgien_pro:pro_join_landing')

@login_required(login_url='account_login')
def dashboard_messages(request):
	if request.user.user_type == 'PRO':
		pro_page = profiles_models.BusinessProfile.objects.get(user=request.user)
		context = {
		"pro_page":pro_page,
		}
		return render(request, 'rehgien_pro/dashboard/messages.html', context)
	else:
		messages.error(request,'Denied. Upgrade to a Pro to continue.')
		return redirect('rehgien_pro:pro_join_landing')


@login_required(login_url='account_login')
def dashboard_insights(request):
	if request.user.user_type == 'PRO':
		pro_page = profiles_models.BusinessProfile.objects.get(user=request.user)
		percentage_rating = 0
		if pro_page.average_rating:
			percentage_rating = pro_page.average_rating / 5 * 100
		context = {
		"pro_page":pro_page,
		"percentage_rating":percentage_rating,
		}
		return render(request, 'rehgien_pro/dashboard/insights.html', context)
	else:
		messages.error(request,'Denied. Upgrade to a Pro to continue.')
		return redirect('rehgien_pro:pro_join_landing')

@login_required(login_url='account_login')
def dashboard_properties(request):
	if request.user.user_type == 'PRO':
		location_name_in = str(request.POST.get('location_name_in', '')).lower()
		listing_type_in = str(request.POST.get('listing_type_in', '')).lower()
		property_type_in = str(request.POST.get('property_type_in', '')).lower()
		active_status_in = str(request.POST.get('active_status_in', '')).lower()

		ImageTransformation = dict(
		format = "jpeg",
		transformation = [
			dict(height=112, width=200, crop="fill",quality="auto", gravity="center",
			format="auto", dpr="auto"),
			]
		)
		pro_page = profiles_models.BusinessProfile.objects.get(user=request.user)

		home_types = listings_models.HomeType.objects.all()

		all_properties = listings_models.Home.objects.all()

		if location_name_in:
			all_properties = all_properties.filter(location_name__icontains = location_name_in)
		if listing_type_in == 'for_sale':
			all_properties = all_properties.filter(listing_type = 'FOR_SALE')
		elif listing_type_in == 'for_rent':
			all_properties = all_properties.filter(listing_type = 'FOR_RENT')

		if property_type_in != 'all' and property_type_in != '':
			all_properties = all_properties.filter(home_type__name__iexact = property_type_in)

		if active_status_in == 'active':
			all_properties = all_properties.filter(is_active = True)
		elif active_status_in == 'inactive':
			all_properties = all_properties.filter(is_active = False)

		user_fs_properties = all_properties.filter(owner=request.user, listing_type = "FOR_SALE")
		user_fr_properties = all_properties.filter(owner=request.user, listing_type = "FOR_RENT")

		filter_fields = {
			"location_name_in":location_name_in,
			"listing_type_in":listing_type_in,
			"property_type_in":property_type_in,
			"active_status_in":active_status_in,
		}
		context = {
		"ImageTransformation":ImageTransformation,
		"pro_page":pro_page,
		"home_types":home_types,
		"all_properties":all_properties,
		"user_fs_properties":user_fs_properties,
		"user_fr_properties":user_fr_properties,
		"filter_fields":filter_fields

		}
		return render(request, 'rehgien_pro/dashboard/property_page.html', context)
	else:
		messages.error(request,'Denied. Upgrade to a Pro to continue.')
		return redirect('rehgien_pro:pro_join_landing')

@login_required(login_url='account_login')
def dashboard_jobs(request):
	if request.user.user_type == 'PRO':
		pro_page = profiles_models.BusinessProfile.objects.get(user=request.user)
		user_job_posts = market_models.JobPost.objects.filter(active=True,job_poster=request.user).order_by('-job_update_date')
		user_jobs_replied = market_models.JobPostProposal.objects.filter(job_post__active=True, proposal_sender=request.user).order_by('-proposal_send_date')

		context = {
		"pro_page":pro_page,
		"user_job_posts":user_job_posts,
		"user_jobs_replied":user_jobs_replied,
		}
		return render(request, 'rehgien_pro/dashboard/jobs.html', context)
	else:
		messages.error(request,'Denied. Upgrade to a Pro to continue.')
		return redirect('rehgien_pro:pro_join_landing')

#other views

def homepage(request):
	if request.user.is_authenticated and request.user.user_type == 'PRO':
		return redirect('rehgien_pro:dashboard_home')
	else:
		return render(request,'rehgien_pro/rehgien_pro_homepage.html',{})

def pro_join_landing(request):
	return render(request,'rehgien_pro/pro_onboarding/landing_page.html',{})

def send_review_request_email(email_dict, message, pk, business_name):
	domain = 'https://' + Site.objects.get_current().domain
	review_page_url = reverse( 'profiles:business_review')
	subject = 'Can you please review me?'
	datalist = []
	extended_message = message + '\n\n' + 'Click this link: ' + domain + review_page_url + '?bsr=' + str(pk) + ' to write your review.' + \
						'\n\n\n' + \
						'Thanks in advance and let me know if you have any questions.' + \
						'\n\n' + \
						'{b_name}'.format(b_name=business_name)
	for email in email_dict:
		datalist.append( (subject, extended_message, '{name} <do-not-reply@rehgien.com>'.format(name=business_name), [email]) )
	try:
		send_mass_mail(tuple(datalist))
	except BadHeaderError:
		return 'Error'
	return 'succcess'

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
			"ProReviewers": "rehgien_pro/pro_onboarding/pro_reviewers.html"
			}

@method_decorator(login_required(login_url='account_login'), name='dispatch')
class ProSetupWizardView(SessionWizardView):
	file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_profile_photos'))

	def dispatch(self, request, *args, **kwargs):
		# check if there is some video onsite
		if profiles_models.BusinessProfile.objects.filter(user = request.user).exists():
			profile_obj = profiles_models.BusinessProfile.objects.get(user = request.user)
			messages.error(request,'You can only own one business profile. Perhaps you wanted to update your current profile.')
			return HttpResponseRedirect(reverse('profiles:pro_business_page_edit', kwargs={'pk':profile_obj.pk}))
		else:
			return super(ProSetupWizardView, self).dispatch(request, *args, **kwargs)

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	# this runs for the step it's on as well as for the step before
	def get_form_initial(self, step):
		current_step = self.storage.current_step
		# get the data for step 0 on step 4
		if step == 'ProReviewers':
			pro_info = self.storage.get_step_data('ProInfo')
			ProServices = self.storage.get_step_data('ProServices')
			ProLocation = self.storage.get_step_data('ProLocation')
			ProBusinessProfileImage = self.storage.get_step_data('ProBusinessProfileImage')
			pro_category_id = pro_info.get('ProInfo-professional_category','')
			pro_category_name = self.get_category_name(pro_category_id)
			business_name = pro_info.get('ProInfo-business_name','')
			innitial = {
			'business_name':business_name,
			'message': "As a {proCat} professional my business heavily depends on recommendations ".format(proCat = pro_category_name) +
						"from clients. Therefore, I would appreciate it if you would write a brief review of me on Rehgien.com," +
						" an influential directory of property and home service professionals."
			}
			return self.initial_dict.get(step, innitial)

		return self.initial_dict.get(step, {})

	def get_category_name(self,pro_category_id):
		try:
			category = profiles_models.ProfessionalCategory.objects.get(pk=int(pro_category_id))
			return category.professional_group.group_name
		except:
			return ''

	def resizePhoto(self,photo,x,y,width,height):
		image = Image.open(photo.file).convert('RGB')
		# The crop method from the Image module takes four coordinates as input.
		# The right can also be represented as (left+width)
		# and lower can be represented as (upper+height).
		cropped_image = image.crop((x, y, width+x, height+y))
		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		output = io.BytesIO()
		resized_image.save(output, format='JPEG', quality=70)
		output.seek(0)
		return InMemoryUploadedFile(output, 'ImageField',
									"%s.jpg" % photo.name.split('.')[0],
									'image/jpeg',
									sys.getsizeof(output), None)

	def done(self, form_list, form_dict, **kwargs):
		ProBusinessProfileImage = form_dict['ProBusinessProfileImage']
		form_data = self.get_all_cleaned_data()
		professional_services = form_data.pop('professional_services')
		service_areas = form_data.pop('service_areas')
		business_profile_image = form_data.pop('business_profile_image')
		x = form_data.pop('x')
		y = form_data.pop('y')
		width = form_data.pop('width')
		height = form_data.pop('height')
		email = form_data.pop('email')
		message = form_data.pop('message')

		resized_image = self.resizePhoto(business_profile_image,x,y,width,height)

		obj_instance = profiles_models.BusinessProfile.objects.create(
						**form_data, business_profile_image = resized_image,
						user=self.request.user,
						)
		obj_instance.professional_services.set(professional_services)
		obj_instance.service_areas.set(service_areas)
		# if everything is setup correctly then update the user type field to pro
		User.objects.filter(pk= self.request.user.pk).update(user_type = 'PRO')

		# then send the review invite emails
		send_review_request_email(email,message, obj_instance.pk, obj_instance.business_name)

		return render(self.request, 'rehgien_pro/pro_onboarding/done.html',{'obj_instance':obj_instance})

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

# Views for Rehgien Agency
def contact_rehgien_agency_team(first_name, last_name, company_name, email, phone, message, service_type):
	try:
		subject = 'You have a new Customer Support Request!'
		plainMessage = "First Name: {fn}. \nLast Name: {ln}. \nCompany: {co}. \nEmail: {e}. \nPhone: {p}. \nService Type: {svc} \n\nMessage: \n\n{m}".format(fn=first_name, ln=last_name, e=email, p=phone, m=message, co=company_name, svc=service_type)

		send_mail(
			subject,
			plainMessage,
			'Rehgien <do-not-reply@rehgien.com>',
			['support@rehgien.com'],
			fail_silently=False,
		)
		return True

	except BadHeaderError:
		return False

def r_agency_home(request):
	if request.method == 'POST':
		contact_form = forms.ContactAgencyTeamForm(request.POST, request.FILES)
		if contact_form.is_valid():
			first_name = contact_form.cleaned_data.get('first_name')
			last_name = contact_form.cleaned_data.get('last_name')
			company_name = contact_form.cleaned_data.get('company_name')
			email = contact_form.cleaned_data.get('email')
			phone = contact_form.cleaned_data.get('phone')
			message = contact_form.cleaned_data.get('message')
			service_type = contact_form.cleaned_data.get('service_type')
			sucess = contact_rehgien_agency_team(first_name, last_name, company_name, email, phone, message,service_type)

			if sucess:
				messages.success(request,"Message Sucessfully Sent!")
			else:
				messages.error(request,"Something went wrong try again later")
		else:
			messages.error(request,"Invalid submission. Check the form for field errors.")
	else:
		contact_form = forms.ContactAgencyTeamForm()

	context = {
		'contactForm':contact_form
	}
	return render(request,'rehgien_pro/rehgien_agency/homepage.html', context)
