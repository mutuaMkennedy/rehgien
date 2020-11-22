from listings import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
					CompanyProfile,
					CompanyReviews,
					AgentProfile,
					AgentReviews,
					PropertyManagerProfile,
					PropertyManagerReviews,
					DesignAndServiceProProfile,
					DesignAndServiceProReviews,
					PMPortfolio,
                    PMPortfolioImages,
                    DesignAndServiceProProjects,
                    DSProProjectImages,
					TeammateConnection
					)
from markets.models import (
                    PropertyRequestLead,
                    ProffesionalRequestLead,
                    OtherServiceLead,
                    AgentLeadRequest,
                    AgentPropertyRequest
                    )
from django.core.exceptions import PermissionDenied
from . import forms
from . import models
from listings import models as listings_models
from django.db.models import Avg
from django.db.models import Prefetch
from django.db.models import Q
from django.forms import modelformset_factory


# referencing the custom user model
User = get_user_model()

# Create your views here.
def check_q_valid(param):
	return param !="" and param is not None

def check_value_valid(param):
	return param <= 5 and param >= 1

def check_service_valid(param):
	return param <= 8 and param >= 1

def home_profile(request):
	agent_profile = AgentProfile.objects.all().filter(user=request.user)
	return render(request, '/templates/base1.html', {'agent_profile':agent_profile})

def profile(request):
	ImageTransformation = dict(
	format = "jpeg",
	transformation = [
		dict(height=112, width=200, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto"),
			]
		)
	user = request.user

	user_sale_posts = listings_models.Home.objects.all().filter(owner=request.user, listing_type='for_sale')
	user_rental_posts =  listings_models.Home.objects.all().filter(owner=request.user, listing_type='for_rent')

	user_sale_favs = user.listings_home_saves_related.filter(listing_type='for_sale')
	user_rental_favs =  user.listings_home_saves_related.filter(listing_type='for_rent')

	#requests
	property_requests = PropertyRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	proffesional_requests = ProffesionalRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	other_requests = OtherServiceLead.objects.all().filter(active=True).filter(owner=request.user)
	ag_lead_requests = AgentLeadRequest.objects.all().filter(active=True).filter(owner=request.user)
	ag_property_requests = AgentPropertyRequest.objects.all().filter(active=True).filter(owner=request.user)

	#porfolio
	pm_portfolio = models.PMPortfolio.objects.all().filter(created_by=request.user)
	project_portfolio = models.DesignAndServiceProProjects.objects.all().filter(created_by=request.user)

	#connections
	user_connections = TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))

	#pros the user has followed
	following = []
	if user.company_followers:
		following += user.company_followers.all()
	if user.agent_followers:
		following += user.agent_followers.all()
	if user.pm_followers:
		following += user.pm_followers.all()
	if user.ds_followers:
		following += user.ds_followers.all()

	#account & profile edit forms
	basic_form = forms.UserEditForm(instance=user)
	ag_bs_form = ''
	pm_bs_form = ''
	ds_bs_form = ''
	co_bs_form = ''
	if user.user_type == 'Agent':
		ag_bs_form = forms.AgentProfileEditForm(instance=user.agent_profile)
	if user.user_type == 'PropertyManager':
		pm_bs_form = forms.PropertyManagerProfileEditForm(instance=user.pm_profile)
	if user.user_type == 'Design&servicePro':
		ds_bs_form = forms.DesignAndServiceProProfileEditForm(instance=user.DService_profile)
	if user.user_type == 'Company':
		co_bs_form = forms.CompanyProfileEditForm(instance=user.company_profile)

	# Pro portfolio & project CU Forms
	PortfolioForm = ''
	ImageForm = ''
	ProjectForm = ''
	ProjectImageForm = ''
	if user.user_type == 'PropertyManager' or user.user_type == 'Company':
		PortfolioForm = forms.PMPortfolioForm()
		ImageForm = forms.PMPortfolioImagesForm()
	if user.user_type == 'Design&servicePro':
		ProjectForm = forms.DesignAndServiceProProjectsForm()
		ProjectImageForm = forms.DSProProjectImagesForm()

	return render(request, 'profiles/user_profile.html', {
	'user': user, 'user_sale_posts':user_sale_posts, 'user_rental_posts':user_rental_posts,
	'user_sale_favs':user_sale_favs, 'user_rental_favs':user_rental_favs, 'ImageTransformation':ImageTransformation,
	"property_requests":property_requests,"proffesional_requests":proffesional_requests,
    "other_requests":other_requests,"ag_lead_requests":ag_lead_requests,"ag_property_requests":ag_property_requests,
	"basic_form":basic_form,"ag_bs_form":ag_bs_form,"pm_bs_form":pm_bs_form,"ds_bs_form":ds_bs_form, 'co_bs_form':co_bs_form,
	"PortfolioForm":PortfolioForm, "ImageForm":ImageForm, "ProjectForm":ProjectForm, "ProjectImageForm":ProjectImageForm,
	"pm_portfolio":pm_portfolio,"project_portfolio":project_portfolio, "user_connections":user_connections,'following':following
	})

@login_required(login_url='account_login')
def edit_basic_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				basic_form = forms.UserEditForm(request.POST, request.FILES, instance=request.user)
				if basic_form.is_valid():
					basic_form.save()

					messages.success(request, 'Profile Updated Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request!')
		else:
			basic_form = forms.UserEditForm(instance=request.user)
	else:
		raise PermissionDenied
	return render(request, 'profiles/user_profile.html', {'basic_form':basic_form})

def business_list(request):
	business_list = CompanyProfile.objects.all()
	featured_b_list = CompanyProfile.objects.filter(featured_business=True)
	location_address = 'Nairobi,Kenya'
	location = request.GET.get('bs-location')
	name = request.GET.get('bs-name-input')
	service = request.GET.get('bs-service-input')
	if check_q_valid(location):
		loc_icontains = location.split(',')
		business_list = business_list.filter(address__icontains = loc_icontains[0])
		featured_b_list = featured_b_list.filter(address__icontains = loc_icontains[0])
		location_address = location
		business_list_count = business_list.count()
	if check_q_valid(name):
		business_list = business_list.filter(	Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		featured_b_list = featured_b_list.filter(Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		name=name
		business_list_count = business_list.count()
	if check_q_valid(service):
		business_list = business_list.filter(speciality__icontains = str(service))
		featured_b_list = featured_b_list.filter(speciality__icontains = service)
		service=service
		business_list_count = business_list.count()
	else:
		business_list = business_list.filter(address__icontains = 'Nairobi')
		featured_b_list = featured_b_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		business_list_count = business_list.count()
	paginator_bs = Paginator(business_list, 3) #show the first 3
	bs_page = request.GET.get('page')
	business_list = paginator_bs.get_page(bs_page)
	return render(request, 'profiles/business_list.html', {
	'business_list':business_list,'location_address':location_address,'name':name, 'service':service,
	'featured_b_list':featured_b_list,'business_list_count':business_list_count
	})

@login_required(login_url='account_login')
def business_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	business = get_object_or_404( CompanyProfile, pk=pk )

	all_connections = TeammateConnection.objects.all()
	pro_teammates = all_connections.filter(Q(requestor=business.user, receiver_accepted = 'No')|Q(receiver = business.user, receiver_accepted = 'No'))

	user_2 = business.user
	user_1 = request.user
	connection_request = all_connections.filter(Q(requestor=user_2, receiver = user_1)|Q(requestor=user_1, receiver = user_2))
	connection = ''
	is_saved = False
	is_following = False
	request_exists = False
	if business.saves.filter(id=request.user.id).exists():
		is_saved = True
	if business.followers.filter(id=request.user.id).exists():
		is_following = True
	if connection_request.exists():
		for connection_object in connection_request:
			connection = connection_object
		request_exists = True

	sale_listings = listings_models.Home.objects.filter(owner=business.user)
	rental_listings = listings_models.Home.objects.filter(owner=business.user)
	management_portfolio = PMPortfolio.objects.filter(created_by = business.user)
	company_reviews = business.company_review.all()
	average_rating = company_reviews.aggregate(Avg('rating'))
	responsive_avg_rating = company_reviews.aggregate(Avg('responsive_rating'))
	knowledge_avg_rating = company_reviews.aggregate(Avg('knowledge_rating'))
	negotiation_avg_rating = company_reviews.aggregate(Avg('negotiation_rating'))
	professionalism_avg_rating = company_reviews.aggregate(Avg('professionalism_rating'))
	reviews_count = company_reviews.count()
	s_count = sale_listings.count()
	r_count = rental_listings.count()
	s_r_total = int(s_count) + int(r_count)
	s_paginator = Paginator(sale_listings, 3) #show the first 3
	sales_page = request.GET.get('page')
	sale_listings_p = s_paginator.get_page(sales_page)
	r_paginator = Paginator(rental_listings, 3) #show the first 3
	rentals_page = request.GET.get('page')
	rental_listings_p = r_paginator.get_page(rentals_page)
	return render(request, 'profiles/business_detail.html', {'business':business, 'sale_listings': sale_listings,
				'rental_listings':rental_listings, 'sale_listings_p':sale_listings_p, 'rental_listings_p':rental_listings_p,
				's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'company_reviews':company_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'responsive_avg_rating':responsive_avg_rating,
				'knowledge_avg_rating':knowledge_avg_rating,'negotiation_avg_rating':negotiation_avg_rating,
				'professionalism_avg_rating':professionalism_avg_rating, 'ImageTransformation':ImageTransformation,
				'management_portfolio':management_portfolio, "is_saved":is_saved, "is_following":is_following,
				"request_exists":request_exists, 'user_2':user_2,"user_1":user_1, "connection": connection,
				"pro_teammates":pro_teammates,
				})

@login_required(login_url='account_login')
def business_review(request):
	if request.method=='POST':
		subject_company = request.POST.get('subject-company')
		rating = request.POST.get('rating-1')
		responsive_rating = request.POST.get('rating-2')
		knowledge_rating = request.POST.get('rating-5')
		negotiation_rating = request.POST.get('rating-4')
		professionalism_rating = request.POST.get('rating-3')
		service = request.POST.get('service-dlv')
		comment = request.POST.get('comment')
		date_of_service = request.POST.get('dos')

		if check_q_valid(subject_company) and check_q_valid(rating
		) and check_q_valid(responsive_rating) and check_q_valid(knowledge_rating
		) and check_q_valid(negotiation_rating) and check_q_valid(professionalism_rating
		) and check_q_valid(comment) and check_q_valid(service) and check_q_valid(date_of_service):

			if CompanyProfile.objects.filter(pk=int(subject_company)).exists():
				if check_value_valid(int(rating)) and check_value_valid(int(responsive_rating)) and check_value_valid(int(knowledge_rating)
				) and check_value_valid(int(negotiation_rating)) and check_value_valid(int(professionalism_rating)
				) and check_service_valid(int(service)):

					company_profile = get_object_or_404(CompanyProfile, pk=int(subject_company))
					review = CompanyReviews.objects.create(
						profile=company_profile,
						rating = int(rating),
						responsive_rating = int(responsive_rating),
						knowledge_rating = int(knowledge_rating),
						negotiation_rating = int(negotiation_rating),
						professionalism_rating = int(professionalism_rating),
						service = str(service),
						comment = str(comment),
						date_of_service = date_of_service,
						user = request.user
						)

					review.save()

					messages.success(request, 'Review posted. Thank you!')
					return redirect(company_profile.get_absolute_url())
				else:
					messages.error(request, 'Value entry does not exist!')
					return redirect('profiles:business_list')
			else:
				messages.error(request,'Business does not exist!')
				return redirect('profiles:business_list')
		else:
			messages.error(request, 'Invalid entry! Make sure you dont have empty entries.')
			return redirect('profiles:business_list')

	elif request.method == 'GET':
		company_id = request.GET.get('bsr')
		if check_q_valid(company_id):
			if CompanyProfile.objects.filter(pk=int(company_id)).exists():
				company = CompanyProfile.objects.get(pk=int(company_id))
				company_reviews = company.company_review.all()
				average_rating = company_reviews.aggregate(Avg('rating'))
				reviews_count = company_reviews.count()
			else:
				messages.error(request,'Business does not exist!')
				return redirect('profiles:business_list')
		else:
			return redirect('profiles:business_list')
	else:
		return redirect('profiles:business_list')
	return render(request, 'profiles/business_review.html',{'company':company, 'average_rating':average_rating, 'reviews_count':reviews_count})

def agent_list(request):
	agent_list = AgentProfile.objects.all().prefetch_related(Prefetch('agent_review', queryset=AgentReviews.objects.all()))
	features_ag_list = AgentProfile.objects.filter(featured_agent=True).prefetch_related(Prefetch('agent_review', queryset=AgentReviews.objects.all()))
	location_address = 'Nairobi,Kenya'
	location = request.GET.get('ag-location')
	name = request.GET.get('ag-name-input')
	service = request.GET.get('ag-service-input')
	if check_q_valid(location):
		loc_icontains = location.split(',')
		agent_list = agent_list.filter(address__icontains = loc_icontains[0])
		features_ag_list = features_ag_list.filter(address__icontains = loc_icontains[0])
		location_address = location
		agent_count = agent_list.count()
	if check_q_valid(name):
		agent_list = agent_list.filter(	Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		features_ag_list = features_ag_list.filter(Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		name=name
		agent_count = agent_list.count()
	if check_q_valid(service):
		agent_list = agent_list.filter(speciality__icontains = str(service))
		features_ag_list = features_ag_list.filter(speciality__icontains = service)
		service = str(service)
		agent_count = agent_list.count()
	else:
		agent_list = agent_list.filter(address__icontains = 'Nairobi')
		features_ag_list = features_ag_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		agent_count = agent_list.count()
	paginator_agents = Paginator(agent_list, 3) #show the first 3
	agents_page = request.GET.get('page')
	agent_list = paginator_agents.get_page(agents_page)
	return render(request, 'profiles/agents_list.html', {
				'agents':agent_list,'location_address':location_address,'service':service,
				'name':name,'features_ag_list':features_ag_list,'agent_count':agent_count
				})

@login_required(login_url='account_login')
def agent_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	agent = get_object_or_404( AgentProfile, pk=pk )

	all_connections = TeammateConnection.objects.all()
	pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

	user_2 = agent.user
	user_1 = request.user
	connection_request = all_connections.filter(Q(requestor=user_2, receiver = user_1)|Q(requestor=user_1, receiver = user_2))
	connection = ''
	is_saved = False
	is_following = False
	request_exists = False
	if agent.saves.filter(id=request.user.id).exists():
		is_saved = True
	if agent.followers.filter(id=request.user.id).exists():
		is_following = True
	if connection_request.exists():
		for connection_object in connection_request:
			connection = connection_object
		request_exists = True

	sale_listings = listings_models.Home.objects.filter(owner=agent.user)
	rental_listings = listings_models.Home.objects.filter(owner=agent.user)
	agent_reviews = agent.agent_review.all()
	average_rating = agent_reviews.aggregate(Avg('rating'))
	responsive_avg_rating = agent_reviews.aggregate(Avg('responsive_rating'))
	knowledge_avg_rating = agent_reviews.aggregate(Avg('knowledge_rating'))
	negotiation_avg_rating = agent_reviews.aggregate(Avg('negotiation_rating'))
	professionalism_avg_rating = agent_reviews.aggregate(Avg('professionalism_rating'))
	reviews_count = agent_reviews.count()
	s_count = sale_listings.count()
	r_count = rental_listings.count()
	s_r_total = int(s_count) + int(r_count)
	s_paginator = Paginator(sale_listings, 3) #show the first 3
	sales_page = request.GET.get('page')
	sale_listings_p = s_paginator.get_page(sales_page)
	r_paginator = Paginator(rental_listings, 3) #show the first 3
	rentals_page = request.GET.get('page')
	rental_listings_p = r_paginator.get_page(rentals_page)
	return render(request, 'profiles/agent_detail.html', {'agent':agent, 'sale_listings': sale_listings,
				'rental_listings':rental_listings, 'sale_listings_p':sale_listings_p, 'rental_listings_p':rental_listings_p,
				's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'agent_reviews':agent_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'responsive_avg_rating':responsive_avg_rating,
				'knowledge_avg_rating':knowledge_avg_rating,'negotiation_avg_rating':negotiation_avg_rating,
				'professionalism_avg_rating':professionalism_avg_rating, 'ImageTransformation':ImageTransformation,
				"is_saved":is_saved, "is_following":is_following,"request_exists":request_exists,
				 "user_2":user_2,"user_1":user_1,"connection": connection, 'pro_teammates':pro_teammates,
				 })

@login_required(login_url='account_login')
def agent_review(request):
	if request.method=='POST':
		subject_agent = request.POST.get('subject-agent')
		rating = request.POST.get('rating-1')
		responsive_rating = request.POST.get('rating-2')
		knowledge_rating = request.POST.get('rating-5')
		negotiation_rating = request.POST.get('rating-4')
		professionalism_rating = request.POST.get('rating-3')
		service = request.POST.get('service-dlv')
		comment = request.POST.get('comment')
		date_of_service = request.POST.get('dos')

		if check_q_valid(subject_agent) and check_q_valid(rating
		) and check_q_valid(responsive_rating) and check_q_valid(knowledge_rating
		) and check_q_valid(negotiation_rating) and check_q_valid(professionalism_rating
		) and check_q_valid(comment) and check_q_valid(service) and check_q_valid(date_of_service):

			if AgentProfile.objects.filter(pk=int(subject_agent)).exists():
				if check_value_valid(int(rating)) and check_value_valid(int(responsive_rating)) and check_value_valid(int(knowledge_rating)
				) and check_value_valid(int(negotiation_rating)) and check_value_valid(int(professionalism_rating)
				) and check_service_valid(int(service)):

					agent_profile = get_object_or_404(AgentProfile, pk=int(subject_agent))
					review = AgentReviews.objects.create(
						profile=agent_profile,
						rating = int(rating),
						responsive_rating = int(responsive_rating),
						knowledge_rating = int(knowledge_rating),
						negotiation_rating = int(negotiation_rating),
						professionalism_rating = int(professionalism_rating),
						service = str(service),
						comment = str(comment),
						date_of_service = date_of_service,
						user = request.user
						)

					review.save()

					messages.success(request, 'Review posted. Thank you!')
					return redirect(agent_profile.get_absolute_url())
				else:
					messages.error(request, 'Value entry does not exist!')
					return redirect('profiles:agent_list')
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:agent_list')
		else:
			messages.error(request, 'Invalid entry! Make sure you dont have empty entries.')
			return redirect('profiles:agent_list')

	elif request.method == 'GET':
		agent_id = request.GET.get('agr')
		if check_q_valid(agent_id):
			if AgentProfile.objects.filter(pk=int(agent_id)).exists():
				agent = AgentProfile.objects.get(pk=int(agent_id))
				agent_reviews = agent.agent_review.all()
				average_rating = agent_reviews.aggregate(Avg('rating'))
				reviews_count = agent_reviews.count()
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:agent_list')
		else:
			return redirect('profiles:agent_list')
	else:
		return redirect('profiles:agent_list')
	return render(request, 'profiles/agent_review.html',{'agent':agent, 'average_rating':average_rating, 'reviews_count':reviews_count})

def property_manager_list(request):
	agent_list = PropertyManagerProfile.objects.all().prefetch_related(Prefetch('pm_review', queryset=PropertyManagerReviews.objects.all()))
	featured_ag_list = PropertyManagerProfile.objects.filter(featured_agent=True).prefetch_related(Prefetch('pm_review', queryset=PropertyManagerReviews.objects.all()))
	location_address = 'Nairobi,Kenya'
	location = request.GET.get('ag-location')
	name = request.GET.get('ag-name-input')
	if check_q_valid(location):
		loc_icontains = location.split(',')
		agent_list = agent_list.filter(address__icontains = loc_icontains[0])
		featured_ag_list = featured_ag_list.filter(address__icontains = loc_icontains[0])
		location_address = location
		agent_count = agent_list.count()
	if check_q_valid(name):
		agent_list = agent_list.filter(	Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		featured_ag_list = featured_ag_list.filter(Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		name=name
		agent_count = agent_list.count()
	else:
		agent_list = agent_list.filter(address__icontains = 'Nairobi')
		featured_ag_list = featured_ag_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		agent_count = agent_list.count()
	paginator_agents = Paginator(agent_list, 3) #show the first 3
	agents_page = request.GET.get('page')
	agent_list = paginator_agents.get_page(agents_page)
	return render(request, 'profiles/property_managers_list.html', {'agents':agent_list, 'location_address':location_address,
				'name':name,'featured_ag_list':featured_ag_list, 'agent_count':agent_count})

@login_required(login_url='account_login')
def property_manager_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	agent = get_object_or_404( PropertyManagerProfile, pk=pk )

	all_connections = TeammateConnection.objects.all()
	pro_teammates = all_connections.filter(Q(requestor=agent.user,receiver_accepted = 'No')|Q(receiver = agent.user,receiver_accepted = 'No'))

	user_2 = agent.user
	user_1 = request.user
	connection_request = all_connections.filter(Q(requestor=user_2, receiver = user_1)|Q(requestor=user_1, receiver = user_2))
	connection = ''
	is_saved = False
	is_following = False
	request_exists = False
	if agent.saves.filter(id=request.user.id).exists():
		is_saved = True
	if agent.followers.filter(id=request.user.id).exists():
		is_following = True
	if connection_request.exists():
		for connection_object in connection_request:
			connection = connection_object
		request_exists = True

	sale_listings = listings_models.Home.objects.filter(owner=agent.user)
	rental_listings = listings_models.Home.objects.filter(owner=agent.user)
	management_portfolio = PMPortfolio.objects.filter(created_by = agent.user)
	agent_reviews = agent.pm_review.all()
	average_rating = agent_reviews.aggregate(Avg('rating'))
	responsive_avg_rating = agent_reviews.aggregate(Avg('responsive_rating'))
	communication_rating = agent_reviews.aggregate(Avg('communication_rating'))
	attention_to_detail = agent_reviews.aggregate(Avg('attention_to_detail'))
	reviews_count = agent_reviews.count()
	s_count = sale_listings.count()
	r_count = rental_listings.count()
	s_r_total = int(s_count) + int(r_count)
	s_paginator = Paginator(sale_listings, 3) #show the first 3
	sales_page = request.GET.get('page')
	sale_listings_p = s_paginator.get_page(sales_page)
	r_paginator = Paginator(rental_listings, 3) #show the first 3
	rentals_page = request.GET.get('page')
	rental_listings_p = r_paginator.get_page(rentals_page)
	return render(request, 'profiles/property_manager_detail.html', {'business':agent, 'sale_listings': sale_listings,
				'rental_listings':rental_listings, 'sale_listings_p':sale_listings_p, 'rental_listings_p':rental_listings_p,
				's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'agent_reviews':agent_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'responsive_avg_rating':responsive_avg_rating,
				'communication_rating':communication_rating,'attention_to_detail':attention_to_detail,
				'ImageTransformation':ImageTransformation, "management_portfolio":management_portfolio,
				"is_saved":is_saved, "is_following":is_following, "user_2":user_2,"user_1":user_1,
				"request_exists":request_exists,"connection": connection, "pro_teammates":pro_teammates,
				})

@login_required(login_url='account_login')
def property_manager_review(request):
	if request.method=='POST':
		subject_agent = request.POST.get('subject-agent')
		rating = request.POST.get('rating-1')
		responsive_rating = request.POST.get('rating-2')
		communication_rating = request.POST.get('rating-3')
		attention_to_detail = request.POST.get('rating-4')
		service = request.POST.get('service-dlv')
		comment = request.POST.get('comment')
		date_of_service = request.POST.get('dos')

		if check_q_valid(subject_agent) and check_q_valid(rating
		) and check_q_valid(responsive_rating) and check_q_valid(communication_rating
		) and check_q_valid(attention_to_detail) and check_q_valid(comment) and check_q_valid(service
		) and check_q_valid(date_of_service):

			if PropertyManagerProfile.objects.filter(pk=int(subject_agent)).exists():
				if check_value_valid(int(rating)) and check_value_valid(int(responsive_rating)) and check_value_valid(int(communication_rating)
				) and check_value_valid(int(attention_to_detail)) and check_service_valid(int(service)):

					agent_profile = get_object_or_404(PropertyManagerProfile, pk=int(subject_agent))
					review = PropertyManagerReviews.objects.create(
						profile=agent_profile,
						rating = int(rating),
						responsive_rating = int(responsive_rating),
						communication_rating = int(communication_rating),
						attention_to_detail = int(attention_to_detail),
						service = str(service),
						comment = str(comment),
						date_of_service = date_of_service,
						user = request.user
						)

					review.save()

					messages.success(request, 'Review posted. Thank you!')
					return redirect(agent_profile.get_absolute_url())
				else:
					messages.error(request, 'Value entry does not exist!')
					return redirect('profiles:pm_list')
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:pm_list')
		else:
			messages.error(request, 'Invalid entry! Make sure you dont have empty entries.')
			return redirect('profiles:pm_list')

	elif request.method == 'GET':
		agent_id = request.GET.get('agr')
		if check_q_valid(agent_id):
			if PropertyManagerProfile.objects.filter(pk=int(agent_id)).exists():
				agent = PropertyManagerProfile.objects.get(pk=int(agent_id))
				agent_reviews = agent.pm_review.all()
				average_rating = agent_reviews.aggregate(Avg('rating'))
				reviews_count = agent_reviews.count()
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:pm_list')
		else:
			return redirect('profiles:pm_list')
	else:
		return redirect('profiles:pm_list')
	return render(request, 'profiles/property_manager_review.html',{'agent':agent, 'average_rating':average_rating, 'reviews_count':reviews_count})

def dservice_pros_list(request):
	pros_list = DesignAndServiceProProfile.objects.all().prefetch_related(Prefetch('DService_review', queryset=DesignAndServiceProReviews.objects.all()))
	featured_pro_list = DesignAndServiceProProfile.objects.filter(featured_pro=True).prefetch_related(Prefetch('DService_review', queryset=DesignAndServiceProReviews.objects.all()))
	location_address = 'Nairobi,Kenya'
	location = request.GET.get('pro-location')
	name = request.GET.get('pro-name-input')
	service = request.GET.get('pro-speciality-input')
	if check_q_valid(location):
		loc_icontains = location.split(',')
		pros_list = pros_list.filter(address__icontains = loc_icontains[0])
		featured_pro_list = featured_pro_list.filter(address__icontains = loc_icontains[0])
		location_address = location
		pros_count = pros_list.count()
	if check_q_valid(name):
		pros_list = pros_list.filter(	Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		featured_pro_list = featured_pro_list.filter(Q(user__first_name__icontains = name)|Q(user__last_name__icontains = name))
		name=name
		pros_count = pros_list.count()
	if check_q_valid(service):
		pros_list = pros_list.filter(pro_speciality__icontains = str(service))
		featured_pro_list = featured_pro_list.filter(pro_speciality__icontains = str(service))
		service = str(service)
		pros_count = pros_list.count()
	else:
		pros_list = pros_list.filter(address__icontains = 'Nairobi')
		featured_pro_list = featured_pro_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		pros_count = pros_list.count()
	paginator_agents = Paginator(pros_list, 3) #show the first 3
	pros_page = request.GET.get('page')
	pros_list = paginator_agents.get_page(pros_page)
	return render(request, 'profiles/other_proffesionals.html', {'pros':pros_list, 'location_address':location_address,
				'name':name,'service':service,'featured_pro_list':featured_pro_list, 'pros_count':pros_count})

@login_required(login_url='account_login')
def dservice_pros_detail(request, pk):
	ImageTransformation = dict(
		format = "jpg",
		transformation = [
			dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
			 format="auto", dpr="auto", fl="progressive"),
				]
			)
	pros = get_object_or_404( DesignAndServiceProProfile, pk=pk )

	all_connections = TeammateConnection.objects.all()
	pro_teammates = all_connections.filter(Q(requestor=pros.user,receiver_accepted = 'No')|Q(receiver = pros.user,receiver_accepted = 'No'))
	user_2 = pros.user
	user_1 = request.user
	connection_request = all_connections.filter(Q(requestor=user_2, receiver = user_1)|Q(requestor=user_1, receiver = user_2))
	connection = ''
	is_saved = False
	is_following = False
	request_exists = False
	if pros.saves.filter(id=request.user.id).exists():
		is_saved = True
	if pros.followers.filter(id=request.user.id).exists():
		is_following = True
	if connection_request.exists():
		for connection_object in connection_request:
			connection = connection_object
		request_exists = True

	pros_reviews = pros.DService_review.all()
	project_portfolio = DesignAndServiceProProjects.objects.filter(created_by = pros.user)
	projects_count = project_portfolio.count()
	average_rating = pros_reviews.aggregate(Avg('rating'))
	quality_avg_rating = pros_reviews.aggregate(Avg('quality_rating'))
	creativity_avg_rating = pros_reviews.aggregate(Avg('creativity_rating'))
	attention_to_detail = pros_reviews.aggregate(Avg('attention_to_detail'))
	reviews_count = pros_reviews.count()
	return render(request, 'profiles/other_proffesionals_detail.html', {'pro':pros, 'pros_reviews':pros_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'quality_avg_rating':quality_avg_rating,
				'attention_to_detail':attention_to_detail,'ImageTransformation':ImageTransformation,
				"project_portfolio":project_portfolio, "is_saved":is_saved, "is_following":is_following,
				"projects_count":projects_count, "user_2":user_2,"user_1":user_1,"request_exists":request_exists,
				"connection": connection,'pro_teammates':pro_teammates
				})

@login_required(login_url='account_login')
def dservice_pros_review(request):
	if request.method=='POST':
		subject_pro = request.POST.get('subject-pro')
		rating = request.POST.get('rating-1')
		quality_rating = request.POST.get('rating-2')
		creativity_rating = request.POST.get('rating-3')
		attention_to_detail = request.POST.get('rating-4')
		comment = request.POST.get('comment')
		date_of_service = request.POST.get('dos')

		if check_q_valid(subject_pro) and check_q_valid(rating
		) and check_q_valid(quality_rating) and check_q_valid(creativity_rating
		) and check_q_valid(attention_to_detail) and check_q_valid(comment
		) and check_q_valid(date_of_service):

			if DesignAndServiceProProfile.objects.filter(pk=int(subject_pro)).exists():
				if check_value_valid(int(rating)) and check_value_valid(int(quality_rating)) and check_value_valid(int(creativity_rating)
				) and check_value_valid(int(attention_to_detail)):

					dservice_profile = get_object_or_404(DesignAndServiceProProfile, pk=int(subject_pro))
					review = DesignAndServiceProReviews.objects.create(
						profile=dservice_profile,
						rating = int(rating),
						quality_rating = int(quality_rating),
						creativity_rating = int(creativity_rating),
						attention_to_detail = int(attention_to_detail),
						comment = str(comment),
						user = request.user
						)

					review.save()

					messages.success(request, 'Review posted. Thank you!')
					return redirect(dservice_profile.get_absolute_url())
				else:
					messages.error(request, 'Value entry does not exist!')
					return redirect('profiles:d_service_list')
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:d_service_list')
		else:
			messages.error(request, 'Invalid entry! Make sure you dont have empty entries.')
			return redirect('profiles:d_service_list')

	elif request.method == 'GET':
		pro_id = request.GET.get('d&sr')
		if check_q_valid(pro_id):
			if DesignAndServiceProProfile.objects.filter(pk=int(pro_id)).exists():
				pro = DesignAndServiceProProfile.objects.get(pk=int(pro_id))
				pro_reviews = pro.DService_review.all()
				average_rating = pro_reviews.aggregate(Avg('rating'))
				reviews_count = pro_reviews.count()
			else:
				messages.error(request,'Agent does not exist!')
				return redirect('profiles:d_service_list')
		else:
			return redirect('profiles:d_service_list')
	else:
		return redirect('profiles:d_service_list')
	return render(request, 'profiles/other_proffesionals_review.html',{'pro':pro, 'average_rating':average_rating, 'reviews_count':reviews_count})

#Pro projects and portfolios CRUD VIEWS
@login_required(login_url='account_login')
def pm_portfolio_create(request):
	if request.user.user_type =='PropertyManager' or request.user.user_type =='Company':
		if request.method =='POST':
				PortfolioForm = forms.PMPortfolioForm(request.POST, request.FILES)
				ImageForm = forms.PMPortfolioImagesForm(request.POST, request.FILES)
				images = request.FILES.getlist('property_image')#name of field
				# Authenticate form
				if PortfolioForm.is_valid() and ImageForm.is_valid():
					instance = PortfolioForm.save(commit=False)
					instance.created_by = request.user
					instance.save()

					for img in images:
						file_instance = PMPortfolioImages(property_image = img, portfolio=PMPortfolio.objects.get(id=instance.id))
						file_instance.save()
					messages.success(request, 'Post Successfull!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request. Request Invalid.')
		else:
			PortfolioForm = forms.PMPortfolioForm()
			ImageForm = forms.PMPortfolioImagesForm()
	else:
		messages.error(request,'Restricted. You dont have permissions for this request.')
		return redirect('profiles:account')
	return render(request, 'profiles/pro_portfolio_create_form.html', {"PortfolioForm": PortfolioForm, "PoImageForm": ImageForm})

@login_required(login_url='account_login')
def pm_portfolio_update(request, pk):
	listing = get_object_or_404(PMPortfolio, pk=pk)
	image_formset = modelformset_factory(PMPortfolioImages, max_num=1, min_num=1, fields=('property_image',))
	if request.user == listing.created_by:
		if request.method=='POST':
			portfolioForm = forms.PMPortfolioForm(request.POST, request.FILES, instance=listing)
			img_formset = image_formset(request.POST or None, request.FILES or None)
			if portfolioForm.is_valid() and img_formset.is_valid():
				listing = portfolioForm.save(commit=False)
				# Associate listing with user
				listing.created_by = request.user
				# finally save to db
				listing.save()

				i_data = PMPortfolioImages.objects.filter(portfolio=listing)

				for index, i in enumerate(img_formset):
					if i.cleaned_data:
						if i.cleaned_data['id'] is None:
							img = PMPortfolioImages(portfolio=listing, property_image=i.cleaned_data.get('image'))
							img.save()
						# elif i.cleaned_data['image'] is False:
						# 	img = PropertyForSaleImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	img.delete()
						else:
							img = PMPortfolioImages(portfolio=listing, property_image=i.cleaned_data.get('image'))
							p = PMPortfolioImages.objects.get(id=i_data[index].id)
							p.property_image = img.property_image
							p.save()

				messages.success(request, 'Update Successull')
				return redirect('profiles:account')
			else:
				messages.error(request, 'Unable to update. Invalid request')
		else:
			portfolioForm = forms.PMPortfolioForm(instance=listing)
			img_formset = image_formset(queryset = PMPortfolioImages.objects.filter(portfolio=listing))
	else:
		raise PermissionDenied
	return render(request, 'profiles/pro_portfolio_update_form.html', {'u_portfolioForm':portfolioForm, 'PmProject':listing, 'PmProjectImgFormset':img_formset})

@login_required(login_url='account_login')
def DS_project_create(request):
	if request.user.user_type =='Design&servicePro':
		if request.method =='POST':
				ProjectForm = forms.DesignAndServiceProProjectsForm(request.POST, request.FILES)
				ProjectImageForm = forms.DSProProjectImagesForm(request.POST, request.FILES)
				images = request.FILES.getlist('project_image')#name of field
				# Authenticate form
				if ProjectForm.is_valid() and ProjectImageForm.is_valid():
					instance = ProjectForm.save(commit=False)
					instance.created_by = request.user
					instance.save()

					for img in images:
						file_instance = DSProProjectImages(project_image = img, project=DesignAndServiceProProjects.objects.get(id=instance.id))
						file_instance.save()
					messages.success(request, 'Post Successfull!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request. Request Invalid.')
		else:
			ProjectForm = forms.DesignAndServiceProProjectsForm()
			ProjectImageForm = forms.DSProProjectImagesForm()
	else:
		messages.error(request,'Restricted. You dont have permissions for this request.')
		return redirect('profiles:account')
	return render(request, 'profiles/pro_portfolio_create_form.html', {"ProjectForm": ProjectForm, "ProjectImageForm": ProjectImageForm})

@login_required(login_url='account_login')
def DS_project_update(request, pk):
	listing = get_object_or_404(DesignAndServiceProProjects, pk=pk)
	image_formset = modelformset_factory(DSProProjectImages, max_num=1, min_num=1, fields=('project_image',))
	if request.user == listing.created_by:
		if request.method=='POST':
			projectForm = forms.DesignAndServiceProProjectsForm(request.POST, request.FILES, instance=listing)
			img_formset = image_formset(request.POST or None, request.FILES or None)
			if projectForm.is_valid() and img_formset.is_valid():
				listing = projectForm.save(commit=False)
				# Associate listing with user
				listing.created_by = request.user
				# finally save to db
				listing.save()

				i_data = DSProProjectImages.objects.filter(project=listing)

				for index, i in enumerate(img_formset):
					if i.cleaned_data:
						if i.cleaned_data['id'] is None:
							img = DSProProjectImages(project=listing, project_image=i.cleaned_data.get('image'))
							img.save()
						# elif i.cleaned_data['image'] is False:
						# 	img = PropertyForSaleImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	img.delete()
						else:
							img = DSProProjectImages(project=listing, project_image=i.cleaned_data.get('image'))
							p = DSProProjectImages.objects.get(id=i_data[index].id)
							p.project_image = img.project_image
							p.save()

				messages.success(request, 'Update Successull')
				return redirect('profiles:account')
			else:
				messages.error(request, 'Unable to update. Invalid request')
		else:
			projectForm = forms.DesignAndServiceProProjectsForm(instance=listing)
			img_formset = image_formset(queryset = DSProProjectImages.objects.filter(project=listing))
	else:
		raise PermissionDenied
	return render(request, 'profiles/pro_portfolio_update_form.html', {'u_projectForm':projectForm, 'DsProject':listing, 'DsProjectImgFormset':img_formset})

#pro save & follow views

@login_required(login_url='account_login')
def save_company(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_saved = False
		pk = int(request.POST.get('pk'))
		business = get_object_or_404(CompanyProfile, pk=pk)
		if business.user != user:
			has_saved = business.saves.filter(pk=user).exists()
			if has_saved:
				business.saves.remove(user)
				is_saved = False
			else:
				business.saves.add(user)
				is_saved = True
			context = {
			'is_saved':is_saved,
			'business':business,
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-co-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-co-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def follow_company(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_following = False
		pk = int(request.POST.get('pk'))
		business = get_object_or_404(CompanyProfile, pk=pk)
		if business.user != user:
			has_followed = business.followers.filter(pk=user).exists()
			if has_followed:
				business.followers.remove(user)
				is_following = False
			else:
				business.followers.add(user)
				is_following = True
			context = {
			'is_following':is_following,
			'business':business,
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-co-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-co-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def save_agent(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_saved = False
		pk = int(request.POST.get('pk'))
		agent = get_object_or_404(AgentProfile, pk=pk)
		if agent.user != user:
			has_saved = agent.saves.filter(pk=user).exists()
			if has_saved:
				agent.saves.remove(user)
				is_saved = False
			else:
				agent.saves.add(user)
				is_saved = True
			context = {
			'is_saved':is_saved,
			'agent':agent,
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-ag-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':"You are not allowed to perform this action",
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-ag-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def follow_agent(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_following = False
		pk = int(request.POST.get('pk'))
		agent = get_object_or_404(AgentProfile, pk=pk)
		if agent.user != user:
			has_followed = agent.followers.filter(pk=user).exists()
			if has_followed:
				agent.followers.remove(user)
				is_following = False
			else:
				agent.followers.add(user)
				is_following = True
			context = {
			'is_following':is_following,
			'agent':agent,
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-ag-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-ag-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def save_pm(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_saved = False
		pk = int(request.POST.get('pk'))
		agent = get_object_or_404(PropertyManagerProfile, pk=pk)
		if agent.user != user:
			has_saved = agent.saves.filter(pk=user).exists()
			if has_saved:
				agent.saves.remove(user)
				is_saved = False
			else:
				agent.saves.add(user)
				is_saved = True
			context = {
			'is_saved':is_saved,
			'agent':agent,
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-pm-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-pm-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def follow_pm(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_following = False
		pk = int(request.POST.get('pk'))
		agent = get_object_or_404(PropertyManagerProfile, pk=pk)
		if agent.user != user:
			has_followed = agent.followers.filter(pk=user).exists()
			if has_followed:
				agent.followers.remove(user)
				is_following = False
			else:
				agent.followers.add(user)
				is_following = True
			context = {
			'is_following':is_following,
			'agent':agent,
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-pm-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-pm-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def save_ds(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_saved = False
		pk = int(request.POST.get('pk'))
		pro = get_object_or_404(DesignAndServiceProProfile, pk=pk)
		if pro.user != user:
			has_saved = pro.saves.filter(pk=user).exists()
			if has_saved:
				pro.saves.remove(user)
				is_saved = False
			else:
				pro.saves.add(user)
				is_saved = True
			context = {
			'is_saved':is_saved,
			'pro':pro,
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-ds-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/save-ds-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def follow_ds(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_following = False
		pk = int(request.POST.get('pk'))
		pro = get_object_or_404(DesignAndServiceProProfile, pk=pk)
		if pro.user != user:
			has_followed = pro.followers.filter(pk=user).exists()
			if has_followed:
				pro.followers.remove(user)
				is_following = False
			else:
				pro.followers.add(user)
				is_following = True
			context = {
			'is_following':is_following,
			'pro':pro,
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-ds-section.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			context = {
			'error':'You are not allowed to perform this action',
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-ds-section.html', context, request=request)
				return JsonResponse({'form':html})

"""
function that adds a pro to another pro's team. Pros dont get added to a team directly instead a pro
sends a request to the other pro asking join the team, then the team instance object is created.
This function just creates the unaccepted object instance. Approval is done by another function
"""
@login_required(login_url='account_login')
def request_connection(request):
	if request.method == 'POST':
		if request.user.user_type != 'NormalUser':
			#users usernames for creating the model instance
			request_exists = False
			user_1 = request.user
			_user_2 = request.POST.get('user')
			user_2 = User.objects.get(username = _user_2)

			#Users pk's and team_request pk for the lookup
			user_1_pk = request.user.pk
			user_2_pk = User.objects.get(username = user_2)

			#Check if request exists -the lookup
			connection_objects = TeammateConnection.objects.filter(Q(requestor=user_2_pk, receiver = user_1_pk)|Q(requestor=user_1_pk, receiver = user_2_pk))
			connection = ''
			for connection_object in connection_objects:
				connection = connection_object

			if connection:
				# remove the request
				connection.delete()
				request_exists = False
			else: #request does not exist
				# create the request
				if user_1 != user_2:
					_connection = TeammateConnection.objects.create(requestor = user_1, receiver = user_2)
					_connection.save()
					request_exists = True
			context = {
			'request_exists':request_exists,
			'user_2':_user_2,
			"user_1":user_1
			}
			if request.is_ajax():
				html = render_to_string('profiles/add-to-team.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			messages.error(request, 'You are not authorized for this action!')
			return redirect('profiles:account')

# for deleting an accepted connection. Only requested from the connections page
@login_required(login_url='account_login')
def remove_connection(request):
	if request.method == 'POST':
		if request.user.user_type != 'NormalUser':
			#users usernames for creating the model instance
			removed = False
			user_1 = request.user
			_user_2 = str(request.POST.get('user'))
			user_2 = User.objects.get(username = _user_2)
			#Users pk's and team_request pk for the lookup
			user_1_pk = request.user.pk
			user_2_pk = User.objects.get(pk = user_2.pk)

			#Check if request exists -the lookup
			connection_objects = TeammateConnection.objects.filter(Q(requestor=user_2_pk, receiver = user_1_pk)|Q(requestor=user_1_pk, receiver = user_2_pk))
			connection = ''
			for connection_object in connection_objects:
				connection = connection_object

			if connection:
				# remove the request
				connection.delete()
				removed = True

			context = {
			'removed':removed,
			'target_user':_user_2
			}
			if request.is_ajax():
				html = render_to_string('profiles/remove_connetion.html', context, request=request)
				return JsonResponse({'form':html})
		else:
			messages.error(request, 'You are not authorized for this action!')
			return redirect('profiles:account')

@login_required(login_url = 'account_login')
def user_connections(request):
	if request.method =='GET':
		all_connections = TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))
		connections = TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))

		name = str(request.GET.get('_myConName', ''))
		if name !='':
			#check if name is username
			username = User.objects.filter(username = name).exists()
			full_name = User.objects.filter(Q(first_name__icontains = name)|Q(last_name__icontains = name)).exists()

			if username:
				user = User.objects.get(username = name)
				connections = connections.filter(Q(requestor=user.pk)|Q(receiver = user.pk))
			elif full_name:
				user = User.objects.filter(Q(first_name__icontains = name)|Q(last_name__icontains = name))
				connections = connections.filter(
							Q(requestor__first_name__icontains=name)|Q(receiver__first_name__icontains = name)|
							Q(requestor__last_name__icontains=name)|Q(receiver__last_name__icontains = name)
							)
			else:
				connecions = ''
	else:
		return redirect('profiles:account')
		messages.error(request, 'Invalid request')
	return render(request, 'profiles/connections_list.html', {"all_connections":all_connections, 'connections':connections,'name':name})

#Follow/unfollow function. Used in the user account manage followers page
@login_required(login_url='account_login')
def pro_follow(request):
	if request.method == 'POST':
		user = int(request.user.id)
		profile_pk = int(request.POST.get('pk'))
		userType = str(request.POST.get('userType'))
		userLoopIndex = int(request.POST.get('loopIndex'))
		is_follower = False

		if profile_pk != '' and userType != '':
			if userType == 'Agent':
				pro = get_object_or_404(AgentProfile, pk=profile_pk)
				if pro.user != user:
					has_followed = pro.followers.filter(pk=user).exists()
					if has_followed:
						pro.followers.remove(user)
						is_follower = False
					else:
						pro.followers.add(user)
						is_follower = True
					context = {
					'follower':pro.user,
					'following':pro.user,
					'userLoopIndex':userLoopIndex,
					'is_follower':is_follower
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
				else:
					context = {
					'error':'You are not allowed to perform this action',
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
			elif userType == 'PropertyManager':
				pro = get_object_or_404(PropertyManagerProfile, pk=profile_pk)
				if pro.user != user:
					has_followed = pro.followers.filter(pk=user).exists()
					if has_followed:
						pro.followers.remove(user)
						is_follower = False
					else:
						pro.followers.add(user)
						is_follower = True
					context = {
					'follower':pro.user,
					'following':pro.user,
					'userLoopIndex':userLoopIndex,
					'is_follower':is_follower
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
				else:
					context = {
					'error':'You are not allowed to perform this action',
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
			elif userType == 'Design&servicePro':
				pro = get_object_or_404(DesignAndServiceProProfile, pk=profile_pk)
				if pro.user != user:
					has_followed = pro.followers.filter(pk=user).exists()
					if has_followed:
						pro.followers.remove(user)
						is_follower = False
					else:
						pro.followers.add(user)
						is_follower = True
					context = {
					'follower':pro.user,
					'following':pro.user,
					'userLoopIndex':userLoopIndex,
					'is_follower':is_follower
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
				else:
					context = {
					'error':'You are not allowed to perform this action',
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
			elif userType == 'Company':
				pro = get_object_or_404(CompanyProfile, pk=profile_pk)
				if pro.user != user:
					has_followed = pro.followers.filter(pk=user).exists()
					if has_followed:
						pro.followers.remove(user)
						is_follower = False
					else:
						pro.followers.add(user)
						is_follower = True
					context = {
					'follower':pro.user,
					'following':pro.user,
					'userLoopIndex':userLoopIndex,
					'is_follower':is_follower
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
				else:
					context = {
					'error':'You are not allowed to perform this action',
					}
					if request.is_ajax():
						html = render_to_string('profiles/follow-pro-section.html', context, request=request)
						return JsonResponse({'form':html})
			elif userType == 'NormalUser':
				context = {
				'error':'Action is forbidden',
				}
				if request.is_ajax():
					html = render_to_string('profiles/follow-pro-section.html', context, request=request)
					return JsonResponse({'form':html})
		else:
			context = {
			'error':'Invalid values',
			}
			if request.is_ajax():
				html = render_to_string('profiles/follow-pro-section.html', context, request=request)
				return JsonResponse({'form':html})

@login_required(login_url='account_login')
def user_followers(request):
	user = request.user

	#followers
	#only pros can have followers
	if request.user.user_type == 'NormalUser':
		followers = ''
	if request.user.user_type == 'Agent':
		followers = user.agent_profile.followers.all()
	if request.user.user_type == 'PropertyManager':
		followers = user.pm_profile.followers.all()
	if request.user.user_type == 'Design&servicePro':
		followers = user.DService_profile.followers.all()
	if request.user.user_type == 'Company':
		followers = user.company_profile.followers.all()

	#following
	#only pros can be followed
	following = []
	if user.company_followers:
		following += user.company_followers.all()
	if user.agent_followers:
		following += user.agent_followers.all()
	if user.pm_followers:
		following += user.pm_followers.all()
	if user.ds_followers:
		following += user.ds_followers.all()

	return render(request, 'profiles/user_followers_list.html', {'followers':followers, 'my_following':following})
