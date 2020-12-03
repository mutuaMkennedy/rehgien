from listings import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

def account_page(request):
	ImageTransformation = dict(
	format = "jpeg",
	transformation = [
		dict(height=112, width=200, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto"),
			]
		)
	user = request.user

	user_sale_posts = listings_models.Home.objects.all().filter(owner=request.user, listing_type__icontains='FOR_SALE')
	user_rental_posts =  listings_models.Home.objects.all().filter(owner=request.user, listing_type__icontains='FOR_SALE')

	user_sale_favs = user.listings_home_saves_related.filter(listing_type__icontains='FOR_SALE')
	user_rental_favs =  user.listings_home_saves_related.filter(listing_type__icontains='FOR_SALE')

	#requests
	property_requests = PropertyRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	proffesional_requests = ProffesionalRequestLead.objects.all().filter(active=True).filter(owner=request.user)
	other_requests = OtherServiceLead.objects.all().filter(active=True).filter(owner=request.user)
	ag_lead_requests = AgentLeadRequest.objects.all().filter(active=True).filter(owner=request.user)
	ag_property_requests = AgentPropertyRequest.objects.all().filter(active=True).filter(owner=request.user)

	#porfolio
	portfolio_items = models.PortfolioItem.objects.all().filter(created_by=request.user)
	porfolio_categories = []
	for choice in models.PortfolioItem.PORTFOLIO_ITEM_TYPE_CHOICE:
		porfolio_categories.append(choice[0].replace('_',' '))

	#connections
	pro_connections = models.TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))

	#pros the user is following
	following = user.business_page_followers.all()

	#account & profile edit forms
	user_account_form = forms.UserEditForm(instance=user)

	return render(request, 'profiles/user_profile.html', {
	'user': user, 'user_sale_posts':user_sale_posts, 'user_rental_posts':user_rental_posts,
	'user_sale_favs':user_sale_favs, 'user_rental_favs':user_rental_favs, 'ImageTransformation':ImageTransformation,
	"property_requests":property_requests,"proffesional_requests":proffesional_requests,
    "other_requests":other_requests,"ag_lead_requests":ag_lead_requests,"ag_property_requests":ag_property_requests,
	"user_account_form":user_account_form,"pro_connections":pro_connections,'following':following,
	'portfolio_items':portfolio_items,'porfolio_categories':porfolio_categories
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

def business_list(request, slug):
	if slug !='':
		type_of_pro = slug.replace('-', ' ')
		print(type_of_pro)
		business_list = models.BusinessProfile.objects.filter(pro_speciality__iexact= type_of_pro)
		featured_b_list = models.BusinessProfile.objects.filter(pro_speciality__iexact = type_of_pro, featured=True)
		_related_services = []
		for business in business_list:
			_related_services += business.get_services_display().split(',')
		related_services = list(set(_related_services)) #removing dulpicate words
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
			business_list = business_list.filter(business_name__icontains = name)
			featured_b_list = featured_b_list.filter(business_name__icontains = name)
			name=name
			business_list_count = business_list.count()
		if check_q_valid(service):
			business_list = business_list.filter(pro_speciality__icontains = str(service))
			featured_b_list = featured_b_list.filter(pro_speciality__icontains = str(service))
			service=service
			business_list_count = business_list.count()
		else:
			business_list = business_list.filter(address__icontains = 'Nairobi')
			featured_b_list = featured_b_list.filter(address__icontains = 'Nairobi')
			location_address = 'Nairobi,Kenya'
			business_list_count = business_list.count()
		paginator_bs = Paginator(business_list, 3)
		bs_page = request.GET.get('page')
		business_list = paginator_bs.get_page(bs_page)
		return render(request, 'profiles/business_list.html', {
		'business_list':business_list,'location_address':location_address,'name':name, 'service':service,
		'featured_b_list':featured_b_list,'business_list_count':business_list_count,
		'type_of_pro':type_of_pro,'slug':slug, 'related_services':related_services
		})
	else:
		messages.error(request, 'The path you requested does not exist')
		return redirect('listings:homepage')

@login_required(login_url='account_login')
def business_detail(request, pk):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)
	business = get_object_or_404( models.BusinessProfile, pk=pk )

	all_connections = models.TeammateConnection.objects.all()
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
	management_portfolio = models.PortfolioItem.objects.filter(created_by = business.user)
	pro_reviews = business.pro_business_review.all()

	average_rating = pro_reviews.aggregate(Avg('rating'))
	responsive_avg_rating = pro_reviews.aggregate(Avg('responsive_rating'))
	knowledge_avg_rating = pro_reviews.aggregate(Avg('knowledge_rating'))
	negotiation_avg_rating = pro_reviews.aggregate(Avg('negotiation_rating'))
	professionalism_avg_rating = pro_reviews.aggregate(Avg('professionalism_rating'))
	reviews_count = pro_reviews.count()
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
				's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'pro_reviews':pro_reviews,
				'reviews_count':reviews_count, 'average_rating':average_rating, 'responsive_avg_rating':responsive_avg_rating,
				'knowledge_avg_rating':knowledge_avg_rating,'negotiation_avg_rating':negotiation_avg_rating,
				'professionalism_avg_rating':professionalism_avg_rating, 'ImageTransformation':ImageTransformation,
				'management_portfolio':management_portfolio, "is_saved":is_saved, "is_following":is_following,
				"request_exists":request_exists, "connection": connection,
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


#Pro projects and portfolios CRUD VIEWS
@login_required(login_url='account_login')
def portfolio_item_create(request, slug):
	if request.user.user_type =='PRO':
		if request.method =='POST':
			category_type = slug
			PortfolioForm = forms.PortfolioItemForm(request.POST, request.FILES)
			ImageForm = forms.PortfolioItemPhotoForm(request.POST, request.FILES)
			images = request.FILES.getlist('photo')#name of field
			# Authenticate form
			if PortfolioForm.is_valid() and ImageForm.is_valid():
				instance = PortfolioForm.save(commit=False)
				instance.created_by = request.user
				instance.save()

				for img in images:
					file_instance = PortfolioItemPhotoForm(property_image = img, portfolio=models.PortfolioItem.objects.get(id=instance.id))
					file_instance.save()
				messages.success(request, 'Post Successfull!')
				return redirect('profiles:account')
			else:
				messages.error(request,'Could not complete request. Request Invalid.')
		else:
			if slug == 'category':
				category_type = request.GET.get('_ptf-catg-choice')
				PortfolioForm = forms.PortfolioItemForm()
				ImageForm = forms.PortfolioItemPhotoForm()
			else:
				messages.error(request,'Invalid path request.')
				return redirect('profiles:account')
	else:
		messages.error(request,'Restricted. You dont have permissions for this request.')
		return redirect('profiles:account')
	return render(request, 'profiles/pro_portfolio_create_form.html', {"PortfolioForm": PortfolioForm, "PoImageForm": ImageForm,
                    'category_type':category_type})

@login_required(login_url='account_login')
def portfolio_item_update(request, pk):
	portfolio_object = get_object_or_404(models.PortfolioItem, pk=pk)
	image_formset = modelformset_factory(forms.PortfolioItemPhotoForm, max_num=1, min_num=1, fields=('photo',))
	if request.user == portfolio_object.created_by:
		if request.method=='POST':
			portfolioForm = forms.PortfolioItemForm(request.POST, request.FILES, instance=portfolio_object)
			img_formset = image_formset(request.POST or None, request.FILES or None)
			if portfolioForm.is_valid() and img_formset.is_valid():
				portfolio_object = portfolioForm.save(commit=False)
				# Associate listing with user
				portfolio_object.created_by = request.user
				# finally save to db
				portfolio_object.save()

				i_data = models.PortfolioItemPhoto.objects.filter(portfolio_item=portfolio_object)

				for index, i in enumerate(img_formset):
					if i.cleaned_data:
						if i.cleaned_data['id'] is None:
							img = models.PortfolioItemPhoto(portfolio_item=portfolio_object, photo=i.cleaned_data.get('photo'))
							img.save()
						# elif i.cleaned_data['image'] is False:
						# 	img = PropertyForSaleImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	img.delete()
						else:
							img = models.PortfolioItemPhoto(portfolio_item=listing, photo=i.cleaned_data.get('photo'))
							p = models.PortfolioItemPhoto.objects.get(id=i_data[index].id)
							p.photo = img.photo
							p.save()

				messages.success(request, 'Update Successull')
				return redirect('profiles:account')
			else:
				messages.error(request, 'Unable to update. Invalid request')
		else:
			portfolioForm = forms.PortfolioItemForm(instance=portfolio_object)
			img_formset = image_formset(queryset = models.PortfolioItemPhoto.objects.filter(portfolio_item=portfolio_object))
	else:
		raise PermissionDenied
	return render(request, 'profiles/pro_portfolio_update_form.html', {'PortfolioForm':portfolioForm, 'portfolio_object':portfolio_object, 'PoImageForm':img_formset})

@login_required(login_url='account_login')
def pro_save(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_saved = False
		pk = int(request.POST.get('pk'))
		pro = get_object_or_404(models.BusinessProfile, pk=pk)
		business_name = 'pro'
		if pro.business_name:
			business_name = pro.business_name

		has_saved = pro.saves.filter(pk=user).exists()
		if has_saved:
			pro.saves.remove(user)
			is_saved = False
			message = "Successfully removed " + business_name +" from saves!"
		else:
			pro.saves.add(user)
			is_saved = True
			message = "Successfully added " + business_name +" to saves!"
		context = {
		'is_saved':is_saved,
		'pro':pro,
		'message':message
		}
		if request.is_ajax():
			html = render_to_string('profiles/pro-save-section.html', context, request=request)
			return JsonResponse({'form':html, 'message':message})
	else:
		err_message = 'Request method not allowed'
		context = {
		'error':'You are not allowed to perform this action',
		'err_message':err_message
		}
		if request.is_ajax():
			html = render_to_string('profiles/pro-save-section.html', context, request=request)
			return JsonResponse({'form':html,'err_message':err_message})

@login_required(login_url='account_login')
def pro_follow(request):
	if request.method == 'POST':
		user = int(request.user.id)
		is_following = False
		pk = int(request.POST.get('pk'))
		pro = get_object_or_404(models.BusinessProfile, pk=pk)
		follower_count = pro.followers.count()
		business_name = 'pro'
		if pro.business_name:
			business_name = pro.business_name

		has_followed = pro.followers.filter(pk=user).exists()
		if has_followed:
			pro.followers.remove(user)
			follower_count = pro.followers.count()
			is_following = False
			message = "Successfully unfollowed " + business_name + '!'
			alert_message = 'You unfollowed ' + business_name + '. Unfollowed pros clear on page reload.'
		else:
			pro.followers.add(user)
			follower_count = pro.followers.count()
			is_following = True
			message = "Successfully followed " + business_name + '!'
			alert_message = 'You followed ' + business_name + '.'

		context = {
		'is_following':is_following,
		'pro':pro,
		'follower_count':follower_count,
		'message':message,
		'alert_message':alert_message
		}
		if request.is_ajax():
			html = render_to_string('profiles/pro-follow-section.html', context, request=request)
			return JsonResponse({'form':html, 'message':message,'alert_message':alert_message, 'follower_count':follower_count})
	else:
		err_message = 'Request method not allowed'
		context = {
		'error':'You are not allowed to perform this action',
		'err_message':err_message
		}
		if request.is_ajax():
			html = render_to_string('profiles/pro-follow-section.html', context, request=request)
			return JsonResponse({'form':html,'err_message':err_message})


"""
function that adds a pro to another pro's team connection list.
Here we just create the unaccepted object instance. Approval is done by another function
"""
@login_required(login_url='account_login')
def request_connection(request):
	if request.method == 'POST':
		if request.user.user_type == 'PRO':
			#users usernames for creating the model instance
			request_exists = False
			requestor = request.user
			_receiver = request.POST.get('user')
			receiver = User.objects.get(username = _receiver)

			# requestor and receivers pk
			requestor_pk = request.user.pk
			receiver_pk = User.objects.get(username = receiver)

			#Check if request exists
			connection_objects = models.TeammateConnection.objects.filter(Q(requestor= requestor_pk, receiver = receiver_pk)|Q(requestor=requestor_pk, receiver = receiver_pk))
			connection = ''
			for connection_object in connection_objects:
				connection = connection_object

			if connection:
				#remove the request
				connection.delete()
				request_exists = False
				message = "Sucessfully removed connection!"
			else:
				# create the request
				if requestor != receiver:
					_connection = models.TeammateConnection.objects.create(requestor = requestor, receiver = receiver)
					_connection.save()
					request_exists = True
					message = "Connection request sent successfully!"
			context = {
			'request_exists':request_exists,
			'receiver':_receiver,
			"requestor":requestor,
			"message":message
			}
			if request.is_ajax():
				html = render_to_string('profiles/add-to-team.html', context, request=request)
				return JsonResponse({'form':html, 'message':message})
		else:
			message = "Invalid request. Method not allowed!"
			if request.is_ajax():
				html = render_to_string('profiles/add-to-team.html', context, request=request)
				return JsonResponse({'form':html})

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
			connection_objects = models.TeammateConnection.objects.filter(Q(requestor=user_2_pk, receiver = user_1_pk)|Q(requestor=user_1_pk, receiver = user_2_pk))
			connection = ''
			for connection_object in connection_objects:
				connection = connection_object

			if connection:
				# remove the request
				connection.delete()
				removed = True
				message = "Sucessfully removed connection!"
				connection=''
			else:
				# create the request
				if user_1 != user_2:
					_connection = models.TeammateConnection.objects.create(requestor = user_1, receiver = user_2)
					_connection.save()
					removed = False
					message = "Connection request sent successfully!"
					connection = _connection
			context = {
			'removed':removed,
			'target_user':user_2,
            'connection':connection,
            'message':message
			}
			if request.is_ajax():
				html = render_to_string('profiles/remove_connection.html', context, request=request)
				return JsonResponse({'form':html, 'message':message})
		else:
			messages.error(request, 'You are not authorized for this action!')
			return redirect('profiles:account')

@login_required(login_url = 'account_login')
def user_connections(request):
	if request.method =='GET':
		all_connections = models.TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))
		connections = models.TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'No')|Q(receiver = request.user, receiver_accepted = 'No'))
        #filtering
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

@login_required(login_url='account_login')
def user_followers(request):
	# The pro's followers
    # Since only pros can have followers we fetch their followers from their business profile
    # and if the requesting user is not a pro we assign and empty string since
    # non-pro users dont have a business profile so they cant have followers
    # Therefore we return an instance of the pro users
	followers = ''
	if request.user.user_type == 'PRO':
		followers = request.user.pro_business_profile.followers.all()

	# The user's following
	# any user can follow a pro i.e. even pros can follow each other
    # So here we just fetch all the business pages the user is followng
    # Therefore we return an instance of the profile object
	following = ''
	if request.user.business_page_followers:
		following = request.user.business_page_followers.all()

	return render(request, 'profiles/user_followers_list.html', {'followers':followers, 'my_following':following})
