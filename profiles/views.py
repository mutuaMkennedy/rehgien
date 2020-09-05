from django.shortcuts import render, get_object_or_404
from listings.models import PropertyForSale
from listings.models import RentalProperty
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
					AgentProfile,
					AgentReviews,
					PropertyManagerProfile,
					PropertyManagerReviews,
					DesignAndServiceProProfile,
					DesignAndServiceProReviews
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
from django.db.models import Avg
from django.db.models import Prefetch
from django.db.models import Q

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
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto"),
			]
		)
	user = request.user
	for_sale_user_posts = PropertyForSale.objects.all().filter(owner=request.user)
	rental_user_posts = RentalProperty.objects.all().filter(owner=request.user)
	user_sale_favourites = user.favourite.all()
	user_rental_favourites = user.rental_favourite.all()
	for_sale = PropertyForSale.objects.all()
	# sale favourites pagination
	paginator_favs = Paginator(user_sale_favourites, 3) #show the first 3
	favs_page = request.GET.get('page')
	user_sale_favs = paginator_favs.get_page(favs_page)
	# rental favourites pagination
	paginator_rental_favs = Paginator(user_rental_favourites, 3) #show the first 3
	rental_favs_page = request.GET.get('page')
	user_rental_favs = paginator_rental_favs.get_page(rental_favs_page)
	#SALES PAGINATION
	paginator_sales = Paginator(for_sale_user_posts, 3) #show the first 3
	listing_page = request.GET.get('page')
	user_sale_posts = paginator_sales.get_page(listing_page)
	#RENTALS PAGINATION
	paginator_rentals = Paginator(rental_user_posts, 3) #show the first 3
	_listing_page = request.GET.get('page')
	user_rental_posts = paginator_rentals.get_page(_listing_page)

	#requests
	property_requests = PropertyRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	proffesional_requests = ProffesionalRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	other_requests = OtherServiceLead.objects.all().filter(active=True).filter(owner=request.user)
	ag_lead_requests = AgentLeadRequest.objects.all().filter(active=True).filter(owner=request.user)
	ag_property_requests = AgentPropertyRequest.objects.all().filter(active=True).filter(owner=request.user)

	return render(request, 'profiles/user_profile.html', {
	'user': user, 'user_sale_posts':user_sale_posts, 'user_rental_posts':user_rental_posts,
	'user_sale_favs':user_sale_favs, 'user_rental_favs':user_rental_favs, 'ImageTransformation':ImageTransformation,
	"property_requests":property_requests,"proffesional_requests":proffesional_requests,
    "other_requests":other_requests,"ag_lead_requests":ag_lead_requests,"ag_property_requests":ag_property_requests
	})

def agent_list(request):
	agent_list = AgentProfile.objects.all().prefetch_related(Prefetch('agent_review', queryset=AgentReviews.objects.all()))
	features_ag_list = AgentProfile.objects.filter(featured_agent=True).prefetch_related(Prefetch('agent_review', queryset=AgentReviews.objects.all()))
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
	else:
		agent_list = agent_list.filter(address__icontains = 'Nairobi')
		features_ag_list = features_ag_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		agent_count = agent_list.count()
	paginator_agents = Paginator(agent_list, 3) #show the first 3
	agents_page = request.GET.get('page')
	agent_list = paginator_agents.get_page(agents_page)
	return render(request, 'profiles/agents_list.html', {'agents':agent_list, 'location_address':location_address,
				'name':name,'features_ag_list':features_ag_list, 'agent_count':agent_count})

def agent_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	agent = get_object_or_404( AgentProfile, pk=pk )
	sale_listings = PropertyForSale.objects.filter(owner=agent.user)
	rental_listings = RentalProperty.objects.filter(owner=agent.user)
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
				'professionalism_avg_rating':professionalism_avg_rating, 'ImageTransformation':ImageTransformation})

@login_required(login_url='account_login')
def edit_n_user_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				nu_edit_form = forms.UserEditForm(request.POST, instance=request.user)
				nup_edit_form = forms.NormalUserProfileEditForm(request.POST, request.FILES,
								instance=request.user.n_user_profile)
				if nup_edit_form.is_valid() and nu_edit_form.is_valid():
					nu_edit_form.save()
					nup_edit_form.save()

					messages.success(request, 'Profile Updated Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request!')
		else:
			nu_edit_form = forms.UserEditForm(instance=request.user)
			nup_edit_form = forms.NormalUserProfileEditForm(instance=request.user.n_user_profile)
	else:
		raise PermissionDenied
	return render(request, 'profiles/edit_profile.html', {'nup_edit_form':nup_edit_form,
	 			'nu_edit_form':nu_edit_form})

@login_required(login_url='account_login')
def edit_agent_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				u_edit_form = forms.UserEditForm(request.POST, instance=request.user)
				p_edit_form = forms.AgentProfileEditForm(request.POST, request.FILES, \
								instance=request.user.agent_profile)
				if p_edit_form.is_valid() and u_edit_form.is_valid():
					u_edit_form.save()
					p_edit_form.save()

					messages.success(request, 'Profile Updated Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request!')
		else:
			u_edit_form = forms.UserEditForm(instance=request.user)
			p_edit_form = forms.AgentProfileEditForm(instance=request.user.agent_profile)
	else:
		raise PermissionDenied
	return render(request, 'profiles/edit_profile.html', {'p_edit_form':p_edit_form, 'u_edit_form':u_edit_form})

@login_required(login_url='account_login')
def edit_pm_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				pmu_edit_form = forms.UserEditForm(request.POST, instance=request.user)
				pm_edit_form = forms.PropertyManagerProfileEditForm(request.POST, \
								request.FILES, instance=request.user.pm_profile)
				if pm_edit_form.is_valid() and pmu_edit_form.is_valid():
					pmu_edit_form.save()
					pm_edit_form.save()

					messages.success(request, 'Profile Updated Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request!')
		else:
			pmu_edit_form = forms.UserEditForm(instance=request.user)
			pm_edit_form = forms.PropertyManagerProfileEditForm(instance=request.user.pm_profile)
	else:
		raise PermissionDenied
	return render(request, 'profiles/edit_profile.html', {'pm_edit_form':pm_edit_form,
	 				'pmu_edit_form':pmu_edit_form})

@login_required(login_url='account_login')
def edit_ds_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				dsu_edit_form = forms.UserEditForm(request.POST, instance=request.user)
				ds_edit_form = forms.DesignAndServiceProProfileEditForm(request.POST, \
								request.FILES, instance=request.user.DService_profile)
				if ds_edit_form.is_valid() and dsu_edit_form.is_valid():
					dsu_edit_form.save()
					ds_edit_form.save()

					messages.success(request, 'Profile Updated Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request!')
		else:
			dsu_edit_form = forms.UserEditForm(instance=request.user)
			ds_edit_form = forms.DesignAndServiceProProfileEditForm(instance=request.user.DService_profile)
	else:
		raise PermissionDenied
	return render(request, 'profiles/edit_profile.html', {'ds_edit_form':ds_edit_form,
	 				'dsu_edit_form':dsu_edit_form})

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
	location = request.GET.get('ag-location')
	name = request.GET.get('ag-name-input')
	service = request.GET.get('ag-service-input')
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

def property_manager_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	agent = get_object_or_404( PropertyManagerProfile, pk=pk )
	sale_listings = PropertyForSale.objects.filter(owner=agent.user)
	rental_listings = RentalProperty.objects.filter(owner=agent.user)
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
	return render(request, 'profiles/property_manager_detail.html', {'agent':agent, 'sale_listings': sale_listings,
				'rental_listings':rental_listings, 'sale_listings_p':sale_listings_p, 'rental_listings_p':rental_listings_p,
				's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'agent_reviews':agent_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'responsive_avg_rating':responsive_avg_rating,
				'communication_rating':communication_rating,'attention_to_detail':attention_to_detail,
				'ImageTransformation':ImageTransformation})

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

# Design and service proffesionals
def dservice_pros_list(request):
	pros_list = DesignAndServiceProProfile.objects.all().prefetch_related(Prefetch('DService_review', queryset=DesignAndServiceProReviews.objects.all()))
	featured_pro_list = DesignAndServiceProProfile.objects.filter(featured_pro=True).prefetch_related(Prefetch('DService_review', queryset=DesignAndServiceProReviews.objects.all()))
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
	else:
		pros_list = pros_list.filter(address__icontains = 'Nairobi')
		featured_pro_list = featured_pro_list.filter(address__icontains = 'Nairobi')
		location_address = 'Nairobi,Kenya'
		pros_count = pros_list.count()
	paginator_agents = Paginator(pros_list, 3) #show the first 3
	pros_page = request.GET.get('page')
	pros_list = paginator_agents.get_page(pros_page)
	return render(request, 'profiles/other_proffesionals.html', {'pros':pros_list, 'location_address':location_address,
				'name':name,'featured_pro_list':featured_pro_list, 'pros_count':pros_count})

def dservice_pros_detail(request, pk):
	ImageTransformation = dict(
		format = "jpg",
		transformation = [
			dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
			 format="auto", dpr="auto", fl="progressive"),
				]
			)
	pros = get_object_or_404( DesignAndServiceProProfile, pk=pk )
	pros_reviews = pros.DService_review.all()
	average_rating = pros_reviews.aggregate(Avg('rating'))
	quality_avg_rating = pros_reviews.aggregate(Avg('quality_rating'))
	creativity_avg_rating = pros_reviews.aggregate(Avg('creativity_rating'))
	attention_to_detail = pros_reviews.aggregate(Avg('attention_to_detail'))
	reviews_count = pros_reviews.count()
	return render(request, 'profiles/other_proffesionals_detail.html', {'pro':pros, 'pros_reviews':pros_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'quality_avg_rating':quality_avg_rating,
				'attention_to_detail':attention_to_detail,'ImageTransformation':ImageTransformation})

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
