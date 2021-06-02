import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from . import forms
from . import models
from profiles import models as profiles_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views import generic
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
from django.core.paginator import Paginator
import statistics
from .regression import trendline as trend
from django.core.serializers import serialize
from django.db.models import Max
from django.core.signals import request_finished
import datetime
from django.utils import timezone
from django.utils.http import urlencode
from django.db.models import Exists, OuterRef
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from .wizard_storage import MultiFileSessionStorage
from profiles.views import ajax_login_required
#from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
#from haystack.query import SearchQuerySet
# referencing the custom user model
User = get_user_model()

def check_q_valid(param):
	return param !="" and param is not None and param != []

def checkAllValue(param):
	return param == 'All';

def shop_category_homepage(request):
	return render(request, 'listings/shop_categories.html', {})

def homepage(request):
	if request.user.is_authenticated:
		return redirect('profiles:user_is_signed_in_homepage')
	else:
		ImageTransformation = dict(
		format = "jpg",
		transformation = [
			dict(crop="fill",height = 408, width = 250,quality="auto", gravity="center", loading="lazy",
			 format="auto", dpr="auto", fl="progressive:steep"),
				]
			)
		professional_groups = profiles_models.ProfessionalGroup.objects.all()
		popular_services = profiles_models.ProfessionalService.objects.all()[:10]
		recommended_services = profiles_models.ProfessionalService.objects.all()[:10]
		context ={
			"professional_groups":professional_groups,
			"popular_services":popular_services,
			"recommended_services":recommended_services,
			'ImageTransformation':ImageTransformation
		}
		return render(request, 'listings/homey.html', context)

def property_homepage(request):
	onsale_recent = models.Home.objects.filter(listing_type__iexact = 'for_sale').order_by('publishdate')[:6]
	onsale_reversed = reversed(onsale_recent)
	#rentals
	rentals_recent = models.Home.objects.filter(listing_type__iexact = 'for_rent').order_by('publishdate')[:6]
	rentals_reversed = reversed(rentals_recent)
	return render(request, 'listings/find_property_home_page.html', {'onsale_reversed': onsale_reversed,
	 		'rentals_reversed': rentals_reversed})

def post_property(request):
	return render(request, 'listings/post_property_landing.html', {})

def property_listings_results(request, property_category, property_listing_type):
	ImageTransformation = dict(
	format = "jpg",
	transformation = [
		dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto", fl="progressive"),
			]
		)

	listings = ''
	model_object = ''
	home_types = models.HomeType.objects.all()

	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	if property_listing_type == 'for_sale':
		listings = model_object.objects.filter(listing_type__iexact = property_listing_type).order_by('-publishdate', 'price')
		listing_type = 'for_sale'
	elif property_listing_type ==  'for_rent':
		listings = model_object.objects.filter(listing_type__iexact = property_listing_type).order_by('-publishdate', 'price')
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	n_bds_median_price = 0

	#Stats placeholders if no listings
	all_prices_median = 0
	all_prices_trend = 0
	_1bd_median_price = 0
	_1bd_price_trend = 0
	_2bd_median_price = 0
	_2bd_price_trend = 0
	_3bd_plus_median_price = 0
	_3bd_plus_price_trend = 0

	# Check if there are listings and then do the stats anylysis
	if listings:
		all_prices = listings.values_list('price', flat=True).distinct()
		if all_prices:
			all_prices_median = statistics.median(all_prices)
			all_prices_index = list(range(1,len(all_prices)+1)) #adding 1 extra index to compensate for starting range at 1 instead of 0
			all_prices_trend = trend(all_prices_index , all_prices)

		_1bd_price = listings.filter(bedrooms = 1).values_list('price', flat=True).distinct()
		if _1bd_price:
			_1bd_median_price = statistics.median(_1bd_price)
			_1bd_price_index = list(range(1,len(_1bd_price)+1))
			_1bd_price_trend = trend(_1bd_price_index , _1bd_price)

		_2bd_price = listings.filter(bedrooms = 2).values_list('price', flat=True).distinct()
		if _2bd_price:
			_2bd_median_price = statistics.median(_2bd_price)
			_2bd_price_index = list(range(1,len(_2bd_price)+1))
			_2bd_price_trend = trend(_2bd_price_index , _2bd_price)

		_3bd_plus_price = listings.filter(bedrooms__gte = 3).values_list('price', flat=True).distinct()
		if _3bd_plus_price:
			_3bd_plus_median_price = statistics.median(_3bd_plus_price)
			_3bd_plus_price_index = list(range(1,len(_3bd_plus_price)+1))
			_3bd_plus_price_trend = trend(_3bd_plus_price_index , _3bd_plus_price)

	location_address = ''
	# Innitial Filter values
	location = request.GET.get('location', '')
	min_price = request.GET.get('min_price', 0)
	max_price = request.GET.get('max_price', 'All')
	property_type = request.GET.get('property_type', 'All')
	bedrooms = request.GET.get('bedrooms', 0)
	bathrooms = request.GET.get('bathrooms', 0)
	page = request.GET.get('page',1)
	sort = str(request.GET.get('sort','jfy'))
	properties_array = request.GET.getlist('properties_array[]',None)
	properties_array = list(map(int, properties_array))
	openhouse = request.GET.get('openhouse', '')
	vr = request.GET.get('vr', '')

	filter_form_data = request.GET.get('filterFormData', '') # Filter form submitted from the results page via ajax
	filter_params_dict = {}
	if check_q_valid(filter_form_data): #if not empty overwrite some of the innitial filter values above
		formdata = json.loads(filter_form_data)
		for field in formdata:
			filter_params_dict[field["name"]] = field["value"]
		# Here we are overwriting the innitial values corresponding to the data in the form
		location = filter_params_dict['location']
		min_price = filter_params_dict['min_price']
		max_price = filter_params_dict['max_price']
		property_type= filter_params_dict['property_type']
		bedrooms = filter_params_dict['bedrooms']
		bathrooms = filter_params_dict['bathrooms']

	if check_q_valid(location):
		listings = listings.filter(location_name__icontains = str(location.split(',')[0]))
		location_address = location
	else:
		listings = listings.filter(location_name__icontains= 'Nairobi')
		location_address = 'Nairobi,Kenya'
	if check_q_valid(min_price) and check_q_valid(max_price):
		if checkAllValue(max_price): #if max price is set to all.
			max_price_q =  listings.aggregate(Max('price'))
			listings = listings.filter(price__range = (min_price,max_price_q['price__max']))
		else:
			listings = listings.filter(price__range = (min_price,max_price))
	if check_q_valid(property_type):
		if not checkAllValue(property_type):
			listings = listings.filter(home_type__name__icontains=property_type)
	if check_q_valid(bedrooms):
		#filter with beds submitted by user
		listings = listings.filter(bedrooms__gte=bedrooms)

		#finding n-median price for a n-bedroomed house to populate the template's insights bar
		n_bds_median_price = 0
		if listings:
			q_beds = 1 if int(bedrooms) == 0 else int(bedrooms)
			n_bds_prices = listings.filter(bedrooms = int(q_beds)).values_list('price', flat=True).distinct()
			if n_bds_prices:
				n_bds_median_price = statistics.median(n_bds_prices)
	if check_q_valid(bathrooms):
		listings = listings.filter(bathrooms__gte=bathrooms)
	if check_q_valid(properties_array):
		listings = listings.filter(id__in = properties_array)
	if check_q_valid(openhouse):
		if  openhouse == 'yes':
			listings = listings.filter(home_openhouse__isnull=False).distinct()
	if check_q_valid(vr):
		if vr == 'yes':
			listings = listings.exclude(virtual_tour_url__isnull = True).exclude(virtual_tour_url__exact = '')

	# Sorting the results
	if sort == 'jfy':
		listings = listings.order_by('-publishdate', 'price') # default sort with our chosen params
	elif sort == 'newer':
		listings = listings.order_by('-publishdate') # descending sort
	elif sort == 'pricehl':
		listings = listings.order_by('-price')
	elif sort == 'older':
		listings = listings.order_by('publishdate') # ascending sort
	elif sort == 'pricelh':
		listings = listings.order_by('price')
	elif sort == 'beds':
		listings = listings.order_by('bedrooms')
	elif sort == 'baths':
		listings = listings.order_by('bathrooms')
	elif sort == 'sqft':
		listings = listings.order_by('floor_area')
	else:
		listings = listings.order_by('-publishdate', 'price')

	listings_count = listings.count()
	all_listings = listings # This will not be paginated

	# paginating the results
	paginator = Paginator(listings, 20)
	if check_q_valid(page):
		listings = paginator.get_page(page)
	else:
		listings = paginator.get_page(1)

	# We reconstruct our query string object which we use in updating addressbar and in saving search
	search_params = filter_params_dict
	search_params['page'] = page
	search_params['sort'] = sort
	search_params['properties_array'] = properties_array
	query_string = urlencode(search_params)

	# Grouped context data
	insight_stats_context = {
		"Onebd_median_price":_1bd_median_price,
		"Twobd_median_price":_2bd_median_price,
		"Threebd_plus_median_price":_3bd_plus_median_price,
		"all_prices_median":all_prices_median,
		"n_bds_median_price":n_bds_median_price,
		"Onebd_price_trend":_1bd_price_trend,
		"twobd_price_trend":_2bd_price_trend,
		"threebd_plus_price_trend":_3bd_plus_price_trend,
		"all_prices_trend":all_prices_trend
	}
	filter_fields_context = {
		"min_price":min_price,
		"max_price":max_price,
		"property_type":property_type,
		"bedrooms":bedrooms,
		"bathrooms":bathrooms,
		'sort':sort
	}

	return render(request, 'listings/property-listing-page.html', {"home_types":home_types,
			"all_listings":all_listings,'listings':listings, 'listings_count':listings_count,
			"ImageTransformation":ImageTransformation ,"location_address":location_address,
			"insight_stats":insight_stats_context,"filter_fields":filter_fields_context, 'query_string':query_string,
			"property_category":property_category,"property_listing_type":property_listing_type
				})

@login_required(login_url='account_login')
def property_detail(request, property_category, pk):
	ImageTransformation = dict(
	format = "jpeg",
	transformation = [
		dict(height=450, width=640, crop="fill",quality="auto", gravity="center",
		 format="auto", dpr="auto"),
			]
		)
	VideoTransformation = dict(
	format = "mp4",
	transformation = [
		dict(height=360, width=640, crop="pad",quality=100, gravity="center",
		 format="auto", dpr="auto", fallback_content="Your browser does not support HTML5 video tags."),
			]
		)

	model_object = ''
	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	listing = get_object_or_404(model_object, pk=pk)
	images = listing.home_photos.all()
	video = listing.home_video.all()

	#this is only fired when the user has clicked the click to call button
	if request.is_ajax():
		dataType = request.GET.get('dataType');
		context={
			'listing':listing,'images':images, 'videos': video,
			'ImageTransformation':ImageTransformation, 'VideoTransformation':VideoTransformation,
			}
		if dataType == 'phone_number':
			int_object = models.PropertyInteraction.objects.filter(home=listing, user=request.user)
			int_object.update(is_lead = True)
			return JsonResponse({'phone_number':listing.phone})
		elif dataType == 'media_video':
			html = render_to_string('listings/property_video_section.html', context, request=request)
			return JsonResponse({'html':html})
		elif dataType == 'media_vr':
			html = render_to_string('listings/property_vr_section.html', context, request=request)
			return JsonResponse({'html':html})

	# Check whether user has an interation object on the listing then create or update it
	try:
		interaction = get_object_or_404(models.PropertyInteraction, home=listing, user=request.user)
		_views_count = interaction.views_count
		models.PropertyInteraction.objects.filter(home=listing, user=request.user)\
					.update(views_count = _views_count + 1)
	except:
		interaction_obj = models.PropertyInteraction.objects.create(
									home = listing,
									user = request.user,
									has_viewed = True,
									views_count = 1
									)
		interaction_obj.save()
	openhouse_dates = listing.home_openhouse.filter(date__range = ( timezone.now() - datetime.timedelta(hours = 12) , timezone.now() + datetime.timedelta(days = 31) ) )
	happening_today = openhouse_dates.filter(date__range = ( timezone.now() - datetime.timedelta(hours = 12) , timezone.now() + datetime.timedelta(hours = 12) ) )
	is_saved = False
	if listing.saves.filter(id=request.user.id).exists():
		is_saved = True

	return render(request, 'listings/property_detail_page.html', {'listing': listing,'is_saved':is_saved ,'images':images, 'videos': video,
				'ImageTransformation':ImageTransformation, 'VideoTransformation':VideoTransformation, 'openhouse_dates':openhouse_dates,
				'happening_today':happening_today})

@ajax_login_required
def save_property(request):
	if request.method == 'POST':
		model_object = ''
		property_category = request.POST.get('property_category')
		if property_category == 'homes':
			model_object = models.Home
		else:
			messages.error(request, 'The path you requested is invalid!')
			return redirect('listings:homepage')

		user = request.user.id
		is_saved = False
		pk = request.POST.get('pk')
		listing = get_object_or_404(model_object, pk=pk)
		_saved = listing.saves.filter(pk=user).exists()
		if _saved:
			listing.saves.remove(user)
			is_saved = False
		else:
			listing.saves.add(user)
			is_saved = True
		context = {
		'is_saved':is_saved,
		'listing':listing,
		}
		if request.is_ajax():
			html = render_to_string('listings/property_save_section.html', context, request=request)
			return JsonResponse({'form':html, 'is_saved':is_saved,'authenticated':True})
		else:
			return redirect('listings:homepage')
	else:
		context = {
		'is_saved':False,
		'listing':listing,
		}
		if request.is_ajax():
			html = render_to_string('listings/property_save_section.html', context, request=request)
			return JsonResponse({'form':html, 'is_saved':False,'authenticated':True, 'error_message':'Invalid Request!'})
		else:
			messages.error(request, 'Invalid Request!')
			return redirect('listings:homepage')

# This view has been discarded in favor of the ListPropertyWizardView below and
# will be removed together with its corresponding template in future commits
@login_required(login_url='account_login')
def property_listing_form(request):
	if request.user.pro_business_profile.professional_category.professional_group.slug =='real-estate-services' :
		open_house_iformset = inlineformset_factory( models.Home , models.PropertyOpenHouse, forms.OpenHouseForm,
		 					max_num=10, min_num=1, extra=0, can_order = True,can_delete=True, exclude=('home',))
		if request.method =='POST':
				PropertyForm = forms.ListingForm(request.POST, request.FILES)
				PhotoForm = forms.PhotoForm(request.POST, request.FILES)
				images = request.FILES.getlist('photo')#name of field
				VideoForm = forms.VideoForm(request.POST, request.FILES)
				videos = request.FILES.getlist('video')#name of field
				open_house_formset = open_house_iformset(request.POST or None, request.FILES or None)
				# Authenticate form
				if PropertyForm.is_valid() and PhotoForm.is_valid() and VideoForm.is_valid() and open_house_formset.is_valid():
					instance = PropertyForm.save(commit=False)
					# Associate listing with user
					instance.owner = request.user
					# finally save to db
					instance.save()

					open_house_formset.save(commit = False )
					for openhouse in open_house_formset:
						if openhouse.is_valid():
							oph = openhouse.save(commit=False)
							oph.home = models.Home.objects.get(id=instance.id)
							oph.save()

					for img in images:
						file_instance = models.PropertyPhoto(photo = img, home = models.Home.objects.get(id=instance.id))
						file_instance.save()

					for vid in videos:
						file_instance2 = models.PropertyVideo(video = vid, home = models.Home.objects.get(id=instance.id))
						file_instance2.save()
					messages.success(request, 'Your Listing has been posted Successfully!')
					return redirect('rehgien_pro:dashboard_properties')
				else:
					messages.error(request,'Could not complete request. Try again later.')
		else:
			PropertyForm = forms.ListingForm()
			PhotoForm = forms.PhotoForm()
			VideoForm = forms.VideoForm()
			open_house_formset = open_house_iformset()
	else:
		messages.error(request,'Restricted. Your account type is not allowed to access this service.')
		return redirect('homepage')
	return render(request, 'listings/property_listing_form.html', {'PropertyForm': PropertyForm, 'ImageForm': PhotoForm,
	 		'VideoForm':VideoForm,'open_house_formset':open_house_formset})

#property create wizard
oph_formset = inlineformset_factory( models.Home , models.PropertyOpenHouse, forms.OpenHouseForm,
 					max_num=10, min_num=1, extra=0, can_order = True,can_delete=True, exclude=('home',))
photos_formset = inlineformset_factory( models.Home , models.PropertyPhoto, forms.PhotoForm,
				max_num=10, min_num=1, extra=0, can_order = True,can_delete=True, exclude=('home',))
videos_formset = inlineformset_factory(models.Home, models.PropertyVideo, forms.VideoForm,
					max_num=1, min_num=1,extra=0,can_order = True,exclude=('home',)
					)
FORMS = [
			("AddressInfo", forms.AddressInfo),
			("MapPoint", forms.MapPoint),
			("PhotoForm", photos_formset),
			("VideoForm", videos_formset),
			("OpenHouseForm", oph_formset),
			("PropetyFacts", forms.PropetyFacts),
		 ]

TEMPLATES = {
			"AddressInfo": "listings/search_property/location_address_form.html",
			"MapPoint": "listings/search_property/map_point_form.html",
			"PhotoForm": "listings/search_property/photo_form.html",
			"VideoForm": "listings/search_property/video_form.html",
			"OpenHouseForm": "listings/search_property/openhouse_form.html",
			"PropetyFacts": "listings/search_property/property_facts_form.html",
			}

@method_decorator(login_required(login_url='account_login'), name='dispatch')
class ListPropertyWizardView(SessionWizardView):
	file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_property_media'))

	def dispatch(self, request, *args, **kwargs):
		if request.user.user_type == 'PRO' and request.user.pro_business_profile.professional_category.professional_group.slug =='real-estate-services':
			return super(ListPropertyWizardView, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('homepage'))

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	# this runs for the step it's on as well as for the step before
	def get_form_initial(self, step):
		current_step = self.storage.current_step
		# get the data for step 0 on step 4
		if step == 'MapPoint':
			address_info = self.storage.get_step_data('AddressInfo')
			innitial = {
			'location_name':address_info.get('AddressInfo-location_name',''),
			'lat':address_info.get('AddressInfo-lat',''),
			'long':address_info.get('AddressInfo-long',''),
			}
			return self.initial_dict.get(step, innitial)

		return self.initial_dict.get(step, {})

	def done(self, form_list, form_dict, **kwargs):
		form_data = self.get_all_cleaned_data()
		lat = form_data.pop('lat')
		long = form_data.pop('long')
		photoFormset = form_data.pop('formset-PhotoForm')
		videoFormset = form_data.pop('formset-VideoForm')
		openhouseFormset = form_data.pop('formset-OpenHouseForm')
		obj_instance = models.Home.objects.create(
						**form_data,
						owner=self.request.user,
						)
		home_object = models.Home.objects.get(id=obj_instance.id)

		openhouseForm = form_dict['OpenHouseForm']
		for openhouse in openhouseForm:
			if openhouse:
				oph = openhouse.save(commit=False)
				oph.home = home_object
				oph.save()

		photoForm = form_dict['PhotoForm']
		for photo in photoForm:
			if photo:
				photo_instance = photo.save(commit=False)
				photo_instance.home = home_object
				photo_instance.save()

		videoForm = form_dict['VideoForm']
		for video in videoForm:
			if video:
				vid_instance = video.save(commit=False)
				vid_instance.home = home_object
				vid_instance.save()

		messages.success(self.request,'Your Listing has been posted Successfully!')
		return redirect('rehgien_pro:dashboard_properties')

@login_required(login_url='account_login')
def property_update(request, property_category, pk):
	model_object = ''
	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	listing = get_object_or_404(model_object, pk=pk)
	image_iformset = inlineformset_factory( models.Home , models.PropertyPhoto, forms.PhotoForm,
	 					max_num=15, min_num=1, extra=0, can_order = True,can_delete=True, exclude=('home',)
	 					)
	video_iformset = inlineformset_factory(models.Home, models.PropertyVideo, forms.VideoForm,
						max_num=1, min_num=1,extra=0,can_order = True,exclude=('home',)
						)
	open_house_iformset = inlineformset_factory( models.Home , models.PropertyOpenHouse, forms.OpenHouseForm,
	 					max_num=10, min_num=1, extra=0, can_order = True,can_delete=True, exclude=('home',)
	 					)
	if request.user == listing.owner:
		if request.method=='POST':
			PropertyForm = forms.ListingForm(request.POST, request.FILES, instance=listing)
			img_formset = image_iformset(request.POST or None, request.FILES or None, instance=listing)
			vid_formset = video_iformset(request.POST or None, request.FILES or None,  instance=listing)
			open_house_formset = open_house_iformset(request.POST or None, request.FILES or None, instance=listing)
			if PropertyForm.is_valid() and img_formset.is_valid() and vid_formset.is_valid() and open_house_formset.is_valid():
				listing = PropertyForm.save(commit=False)
				listing.owner = request.user
				listing.save()
				img_formset.save()
				vid_formset.save()
				open_house_formset.save()

				messages.success(request, 'Update Successull')
				return redirect('rehgien_pro:dashboard_properties')
			else:
				messages.error(request, 'Unable to update. Make sure no fields are empty')
		else:
			PropertyForm = forms.ListingForm(instance=listing)
			img_formset = image_iformset(instance=listing)
			vid_formset = video_iformset(instance=listing)
			open_house_formset = open_house_iformset(instance=listing)
	else:
		raise PermissionDenied
	return render(request, 'listings/update_form.html', {'PropertyForm':PropertyForm, 'listing':listing,
	 	'img_formset':img_formset, 'vid_formset':vid_formset,'open_house_formset':open_house_formset})

@login_required(login_url='account_login')
def property_delete(request,property_category,pk):
	model_object = ''
	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	listing = get_object_or_404(model_object, pk=pk)
	if request.user == listing.owner:
		listing.delete()
		messages.success(request, 'Successfully deleted!!')
		return redirect('rehgien_pro:dashboard_properties')
	else:
		raise PermissionDenied
		return redirect('rehgien_pro:dashboard_properties')

@login_required(login_url='account_login')
def set_open_house_reminder(request):
	if request.method == 'POST':
		user = request.user.id
		event_id = request.POST.get('openHouseEventId')
		openhouse = get_object_or_404(models.PropertyOpenHouse, pk=event_id)
		_reminder_set = openhouse.reminder_list.filter(pk=user).exists()
		if _reminder_set:
			openhouse.reminder_list.remove(user)
			reminder_set = 'Set reminder'
			message = 'Reminder removed. You will not be alerted on this event.'
		else:
			openhouse.reminder_list.add(user)
			reminder_set = 'Remove reminder'
			message = 'Reminder set. We will alert you when the event nears.'
		if request.is_ajax():
			return JsonResponse({'reminder_set':reminder_set,'message':message,})
	else:
		messages.error(request, 'Invalid Request!')
		return redirect('listings:homepage')

@ajax_login_required
def save_search(request):
	if request.method == 'POST':
		search_query_string = request.POST.get('queryString','')
		# try:
		search_object = models.SavedSearch.objects.create(
			user = request.user,
			search_url = search_query_string
			)
		search_object.save()
		message = 'sucess'
		# except:
		# 	message = 'error'

		if request.is_ajax():
			return JsonResponse({'message':message,'authenticated':True})
		else:
			messages.error(request, 'We can\'t process your request as submited!')
			return redirect('listings:homepage')
	else:
		messages.error(request, 'Invalid Request!')
		return redirect('listings:homepage')
