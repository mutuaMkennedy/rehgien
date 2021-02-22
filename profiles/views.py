from listings import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from markets import models as markets_models
from location import models as location_models
from django.core.exceptions import PermissionDenied
from . import forms
from . import models
from listings import models as listings_models
from django.db.models import Avg,Count
from django.db.models import Prefetch
from django.db.models import Q
from django.forms import modelformset_factory
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
from django.utils.http import urlencode
from django.core.exceptions import ObjectDoesNotExist
from .profile_edit_views import resizePhoto

# referencing the custom user model
User = get_user_model()

# Create your views here.
def check_q_valid(param):
	return param !="" and param is not None

def check_value_valid(param):
	return param <= 5 and param >= 1

def check_service_valid(param):
	return param <= 8 and param >= 1

@login_required(login_url='account_login')
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
	user_rental_posts =  listings_models.Home.objects.all().filter(owner=request.user, listing_type__icontains='FOR_RENT')

	user_sale_favs = user.listings_home_saves_related.filter(listing_type__icontains='FOR_SALE')
	user_rental_favs =  user.listings_home_saves_related.filter(listing_type__icontains='FOR_RENT')

	job_post = markets_models.JobPost.objects.filter(active=True,job_poster=request.user)
	my_job_replies = markets_models.JobPostProposal.objects.filter(job_post__active=True, proposal_sender=request.user)

	#porfolio
	portfolio_items = models.PortfolioItem.objects.all().filter(created_by=request.user)

	#connections
	pro_connections = models.TeammateConnection.objects.filter(Q(requestor=request.user, receiver_accepted = 'Yes')|Q(receiver = request.user, receiver_accepted = 'Yes'))

	#pros the user is following
	following = user.business_page_followers.all()

	#account edit forms
	basic_form = forms.UserEditForm(instance=user)

	return render(request, 'profiles/user_profile.html', {
	'user': user, 'user_sale_posts':user_sale_posts, 'user_rental_posts':user_rental_posts,
	'user_sale_favs':user_sale_favs, 'user_rental_favs':user_rental_favs, 'ImageTransformation':ImageTransformation,
	"job_post":job_post,"my_job_replies":my_job_replies,
	"basic_form":basic_form,"pro_connections":pro_connections,'following':following,
	'portfolio_items':portfolio_items
	})

@login_required(login_url='account_login')
def edit_basic_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
				basic_form = forms.UserEditForm(request.POST, request.FILES, instance=request.user)
				if basic_form.is_valid():
					instance = basic_form.save(commit=False)

					temp_photo = basic_form.cleaned_data['profile_image']
					x = basic_form.cleaned_data.get('x')
					y = basic_form.cleaned_data.get('y')
					w = basic_form.cleaned_data.get('width')
					h = basic_form.cleaned_data.get('height')

					cropped_photo = resizePhoto(temp_photo,x,y,w,h)

					instance.profile_image = cropped_photo
					instance.save()

					context = {
					'user':request.user,
					'basic_form':basic_form
					}
					message = 'Profile Updated Successfully!'
					if request.is_ajax():
						ac_details = render_to_string('profiles/account_details_section.html', context, request=request)
						ac_greet = render_to_string('profiles/account_greet.html', context, request=request)
						profile_completion = render_to_string('profiles/account_completion_section.html', context, request=request)
						return JsonResponse({'ac_details':ac_details ,'ac_greet':ac_greet, 'profile_completion':profile_completion,
							'success':message})
					else:
						return redirect('profiles:account')
				else:
					context = {
					'user':request.user,
					'basic_form':basic_form
					}
					message = 'Invalid submission. Could not update!'
					if request.is_ajax():
						ac_details = render_to_string('profiles/account_details_section.html', context, request=request)
						ac_greet = render_to_string('profiles/account_greet.html', context, request=request)
						profile_completion = render_to_string('profiles/account_completion_section.html', context, request=request)
						return JsonResponse({'ac_details':ac_details ,'ac_greet':ac_greet,'profile_completion':profile_completion,
							'error':message})
					else:
						return redirect('profiles:account')
		else:
			basic_form = forms.UserEditForm(instance=request.user)
	else:
		raise PermissionDenied
		return render(request, 'profiles/user_profile.html', {'basic_form':basic_form})

def business_homepage(request):
	popular_services = models.ProfessionalService.objects.all()[:10]
	recommended_services = models.ProfessionalService.objects.all()[:10]
	pro_group = models.ProfessionalGroup.objects.all()
	context = {
	"popular_services":popular_services,
	"recommended_services":recommended_services,
	"pro_group":pro_group
	}
	return render(request,'profiles/professionals_homepage.html',context)

def ajax_autocomplete(request):
	if request.is_ajax():
		query = str(request.GET.get('term', ''))
		services = models.ProfessionalService.objects.filter(service_name__icontains = query)
		results = []
		for service in services:
			results.append(service.service_name.capitalize())
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def business_list(request):
	all_pro_categories = models.ProfessionalCategory.objects.all()
	all_services = models.ProfessionalService.objects.all()

	business_list = models.BusinessProfile.objects.all()
	featured_b_list = ''

	town_names = []
	for town in location_models.KenyaTown.objects.all():
		town_names.append(town.town_name)

	q_pro_category = str( request.GET.get('p_cat', '') )
	service = str( request.GET.get('q_service', '') )
	location = str( request.GET.get('pro_location', 'Nairobi') )
	job_rating = int( request.GET.get('job_rating',0) )
	sort = str( request.GET.get('sort','') )
	bs_page = request.GET.get('page', '1')

	if check_q_valid(q_pro_category):
		business_list = business_list.filter(professional_category__slug = q_pro_category)
		featured_b_list = business_list.filter(professional_category__slug = q_pro_category, featured=True)
	if check_q_valid(location):
		business_list = business_list.filter(service_areas__town_name__icontains = location)
		featured_b_list = business_list.filter(service_areas__town_name__icontains = location)
		business_list_count = business_list.count()

	if check_q_valid(service):
		business_list = business_list.filter(professional_services__slug__icontains = service)
		featured_b_list = business_list.filter(professional_services__slug__icontains = service)
		business_list_count = business_list.count()
	if check_q_valid(job_rating):
		if job_rating != 0:
			business_list = business_list.annotate(avg_rating=Avg('pro_business_review__recommendation_rating')).filter(avg_rating__gte=job_rating)
			featured_b_list = business_list.annotate(avg_rating=Avg('pro_business_review__recommendation_rating')).filter(avg_rating__gte=job_rating)
			business_list_count = business_list.count()
	if sort == 'mostProjects':
		business_list = business_list.annotate(num_projects=Count('user__profiles_portfolioitem_createdby',distinct=True)).order_by('-num_projects')
	elif sort == 'mostFollowers':
		business_list = business_list.order_by('followers')
	elif sort == 'mostSaved':
		business_list = business_list.order_by('saves')

	paginator_bs = Paginator(business_list, 20)
	business_list = paginator_bs.get_page(bs_page)

	search_params = {}
	search_params['p_cat'] = q_pro_category
	search_params['q_service'] = service
	search_params['pro_location'] = location
	search_params['job_rating'] = job_rating
	search_params['sort'] = sort
	search_params['page'] = bs_page

	query_string = urlencode(search_params)
	q_pro_category = q_pro_category.replace('-',' ')
	return render(request, 'profiles/business_list.html', {
	'business_list':business_list,'featured_b_list':featured_b_list,
	'business_list_count':business_list_count, 'all_services':all_services,
	'all_pro_categories':all_pro_categories,'q_pro_category':q_pro_category,
	'town_names':town_names,"query_string":query_string,'search_params':search_params
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
	business = get_object_or_404( models.BusinessProfile, pk=pk )

	all_connections = models.TeammateConnection.objects.all()
	pro_teammates = all_connections.filter(Q(requestor=business.user, receiver_accepted = 'Yes')|Q(receiver = business.user, receiver_accepted = 'Yes'))

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
	all_listings = listings_models.Home.objects.filter(owner=business.user).order_by('-publishdate')
	sale_listings = all_listings.filter(owner=business.user,listing_type__icontains='FOR_SALE')
	rental_listings = all_listings.filter(owner=business.user,listing_type__icontains='FOR_RENT')
	s_count = sale_listings.count()
	r_count = rental_listings.count()
	s_r_total = int(all_listings.count())

	p_listings_paginator = Paginator(all_listings, 3)
	property_page = request.GET.get('page')
	property_listings_p = p_listings_paginator.get_page(property_page)

	projects = models.PortfolioItem.objects.filter(created_by = business.user).order_by('-created_at')

	# Review objects
	pro_reviews = business.pro_business_review.all().order_by('review_date')

	recommendation_rating_avg = pro_reviews.aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
	responsive_rating_avg = pro_reviews.aggregate(Avg('responsive_rating')).get('responsive_rating__avg', 0.00)
	knowledge_rating_avg = pro_reviews.aggregate(Avg('knowledge_rating')).get('knowledge_rating__avg', 0.00)
	professionalism_rating_avg = pro_reviews.aggregate(Avg('professionalism_rating')).get('professionalism_rating__avg', 0.00)
	quality_of_service_rating_avg = pro_reviews.aggregate(Avg('quality_of_service_rating')).get('quality_of_service_rating__avg', 0.00)

	five_star_ratings = pro_reviews.filter(recommendation_rating=5).count()
	four_star_ratings = pro_reviews.filter(recommendation_rating=4).count()
	three_star_ratings = pro_reviews.filter(recommendation_rating=3).count()
	two_star_ratings = pro_reviews.filter(recommendation_rating=2).count()
	one_star_ratings = pro_reviews.filter(recommendation_rating=1).count()
	rvw_count = pro_reviews.count()
	if rvw_count == 0:
		rvw_count = 1
	five_star_ratings_avg = five_star_ratings/ rvw_count * 100
	four_star_ratings_avg = four_star_ratings / rvw_count * 100
	three_star_ratings_avg = three_star_ratings / rvw_count * 100
	two_star_ratings_avg = two_star_ratings / rvw_count * 100
	one_star_ratings_avg = one_star_ratings / rvw_count * 100

	reviews_count = pro_reviews.count()

	review_page = request.GET.get('review_page','1')
	review_sort = request.GET.get('review_sort','most relevant')

	if review_sort == 'most relevant':
		pro_reviews = pro_reviews.order_by('likes')
	elif review_sort == 'highest rated':
		pro_reviews == pro_reviews.order_by('-recommendation_rating')
	elif review_sort == 'lowest rated':
		pro_reviews = pro_reviews.order_by('recommendation_rating')
	elif review_sort == 'newest first':
		pro_reviews = pro_reviews.order_by('-review_date')
	elif review_sort == 'oldest first':
		pro_reviews = pro_reviews.order_by('review_date')

	review_paginator = Paginator(pro_reviews, 5)
	pro_reviews = review_paginator.get_page(review_page)

	search_params = {}
	search_params['review_sort'] = review_sort
	search_params['review_page'] = review_page

	query_string = urlencode(search_params)

	params_context = {
		'review_sort':review_sort,
	}

	context ={'business':business, "all_listings":all_listings,'property_listings_p':property_listings_p, 'sale_listings': sale_listings,
			'rental_listings':rental_listings,
			's_r_total':s_r_total, 's_count':s_count,'r_count':r_count, 'pro_reviews':pro_reviews,
			'reviews_count':reviews_count, 'recommendation_rating_avg':recommendation_rating_avg, 'responsive_rating_avg':responsive_rating_avg,
			'knowledge_rating_avg':knowledge_rating_avg,'professionalism_rating_avg':professionalism_rating_avg,
			'quality_of_service_rating_avg':quality_of_service_rating_avg, 'ImageTransformation':ImageTransformation,
			'projects':projects, "is_saved":is_saved, "is_following":is_following,
			"request_exists":request_exists, "connection": connection, "five_star_ratings":five_star_ratings,
			"four_star_ratings":four_star_ratings, "three_star_ratings":three_star_ratings,
			"two_star_ratings":two_star_ratings, "one_star_ratings":one_star_ratings,
			"pro_teammates":pro_teammates,'all_listings':all_listings,
			"five_star_ratings_avg":five_star_ratings_avg, "four_star_ratings_avg":four_star_ratings_avg,
			"three_star_ratings_avg":three_star_ratings_avg,"two_star_ratings_avg":two_star_ratings_avg,
			"one_star_ratings_avg":one_star_ratings_avg,"query_string":query_string,"params_context":params_context
			}
	return render(request, 'profiles/business_detail.html', context)

@login_required(login_url='account_login')
def business_review(request):
	if request.method=='POST':
		subject_pro = request.POST.get('pro_id')
		recommendation_rating = request.POST.get('rating-1')
		responsive_rating = request.POST.get('rating-2')
		knowledge_rating = request.POST.get('rating-5')
		professionalism_rating = request.POST.get('rating-3')
		quality_of_service_rating = request.POST.get('rating-4')

		comment = request.POST.get('comment')

		if check_q_valid(subject_pro) and check_q_valid(recommendation_rating
		) and check_q_valid(responsive_rating) and check_q_valid(knowledge_rating
		) and check_q_valid(professionalism_rating) and check_q_valid(quality_of_service_rating
		) and check_q_valid(comment):

			if models.BusinessProfile.objects.filter(pk=int(subject_pro)).exists():
				if check_value_valid(int(recommendation_rating)) and check_value_valid(int(responsive_rating)) and check_value_valid(int(knowledge_rating)
				) and check_value_valid(int(professionalism_rating)) and check_value_valid(int(quality_of_service_rating)):

					pro_profile = get_object_or_404(models.BusinessProfile, pk=int(subject_pro))
					review = models.Review.objects.create(
							profile=pro_profile,
							recommendation_rating = int(recommendation_rating),
							responsive_rating = int(responsive_rating),
							knowledge_rating = int(knowledge_rating),
							professionalism_rating = int(professionalism_rating),
							quality_of_service_rating = int(quality_of_service_rating),
							comment = str(comment),
							reviewer = request.user
							)

					review.save()

					messages.success(request, 'Review posted. Thank you!')
					return redirect(pro_profile.get_absolute_url())
				else:
					messages.error(request, 'Value entry does not exist!')
					return redirect('profiles:business_list')
			else:
				messages.error(request,'The pro you requested does not exist!')
				return redirect('profiles:business_list')
		else:
			messages.error(request, 'Invalid entry! Make sure you dont have empty fields.')
			return redirect('profiles:business_review')

	elif request.method == 'GET':
		subject_pro = request.GET.get('bsr')
		if check_q_valid(subject_pro):
			if models.BusinessProfile.objects.filter(pk=int(subject_pro)).exists():
				pro = models.BusinessProfile.objects.get(pk=int(subject_pro))
				pro_reviews = pro.pro_business_review.all()
				recommendation_rating_avg = pro_reviews.aggregate(Avg('recommendation_rating')).get('recommendation_rating__avg', 0.00)
				reviews_count = pro_reviews.count()
			else:
				messages.error(request,'Business does not exist!')
				return redirect('profiles:business_list')
		else:
			return redirect('profiles:business_list')
	else:
		return redirect('profiles:business_list')
	return render(request, 'profiles/business_review.html',{'pro':pro, 'recommendation_rating_avg':recommendation_rating_avg, 'reviews_count':reviews_count})

@login_required(login_url='account_login')
def like_review(request):
	if request.method == 'POST':
		user_id = request.user.pk
		review_object = request.POST.get('like_review','')
		message = ''
		try:
			review  = get_object_or_404(models.Review, pk= int(review_object))
			if review.likes.filter(pk=user_id).exists():
				review.likes.remove(user_id)
				message = 'Success'
			else:
				review.likes.add(user_id)
				message = 'Success'
			context = {
				"reviews":review,
				}
			if request.is_ajax():
				html = render_to_string('profiles/review_like_section.html', context, request=request)
				return JsonResponse({'form':html, 'message':message})

		except ObjectDoesNotExist as e:
			print(e)
			message = 'Error'
			if request.is_ajax():
				return JsonResponse({'message':message})
	else:
		return redirect('profiles:business_detail')

@login_required(login_url='account_login')
def portfolio_item_create(request):
	if request.user.user_type =='PRO':
		if request.method =='POST':
			PortfolioForm = forms.PortfolioItemForm(request.POST, request.FILES)
			ImageForm = forms.PortfolioItemPhotoForm(request.POST, request.FILES)
			images = [request.FILES.get('photo[%d]' % i) for i in range(0, len(request.FILES))]
			# Authenticate form
			if PortfolioForm.is_valid() and ImageForm.is_valid():
				instance = PortfolioForm.save(commit=False)
				instance.created_by = request.user
				instance.save()

				for img in images:
					file_instance = models.PortfolioItemPhoto(photo = img, portfolio_item=models.PortfolioItem.objects.get(id=instance.id))
					file_instance.save()
				messages.success(request, 'Project adedd Successfully!')
				return redirect('profiles:portfolio_item_create')
			else:
				messages.error(request,'Could not complete request. Request Invalid.')
		else:
			PortfolioForm = forms.PortfolioItemForm()
			ImageForm = forms.PortfolioItemPhotoForm()
	else:
		messages.error(request,'Restricted. You dont have permissions for this request.')
		return redirect('profiles:account')
	return render(request, 'profiles/pro_portfolio_create_form.html', {"PortfolioForm": PortfolioForm, "PoImageForm": ImageForm})

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
Here we just create the unaccepted object instance.
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

def connection_request_action(request):
	if request.method == 'POST':
		if request.user.user_type != 'NormalUser':
			#users usernames for creating the model instance
			removed = False
			object_id = int(request.POST.get('rq_id'))

			try:
				connection_object = get_object_or_404(models.TeammateConnection, pk='object_id')
				if connection_object.receiver == request.user:
					connection_object.delete()
					removed = True
					message = 'Success'
					if request.is_ajax():
						return JsonResponse({'error':message, 'removed':removed})
				else:
					if request.is_ajax():
						message ='Permission Denied!'
						return JsonResponse({'error':message,'removed':removed})
			except:
				message ='Failed. Try again later'
				if request.is_ajax():
					html = render_to_string('profiles/remove_connection.html', context, request=request)
					return JsonResponse({'form':html, 'error':message})
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

@login_required(login_url='account_login')
def notifications(request):
	pending_connections = models.TeammateConnection.objects.filter(
							receiver = request.user ,receiver_accepted = 'No'
						)
	notifications_count = 0
	notifications_count = pending_connections.count()
	context = {
	'pending_connections':pending_connections,
	'notifications_count':notifications_count
	}
	return render(request,'profiles/notifications.html',context)
