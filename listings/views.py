from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from profiles.models import AgentProfile
from . import forms
from . import models
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
#from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
#from haystack.query import SearchQuerySet

# referencing the custom user model
User = get_user_model()

def check_q_valid(param):
	return param !="" and param is not None

def homepage(request):
	onsale_recent = models.Home.objects.filter(listing_type__iexact = 'for_sale').order_by('publishdate')[:6]
	onsale_reversed = reversed(onsale_recent)
	#rentals
	rentals_recent = models.Home.objects.filter(listing_type__iexact = 'for_rent').order_by('publishdate')[:6]
	rentals_reversed = reversed(rentals_recent)
	return render(request, 'listings/homey.html', {'onsale_reversed': onsale_reversed, 'rentals_reversed': rentals_reversed})


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
	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	if property_listing_type == 'for_sale':
		listings = model_object.objects.filter(listing_type__iexact = property_listing_type).order_by('-publishdate', 'price')
		listing_type = 'for_sale'
	elif property_listing_type ==  'for_rent':
		listings = model_object.objects.filter(listing_type = property_listing_type).order_by('-publishdate', 'price')
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
		all_prices_median = statistics.median(all_prices)
		all_prices_index = list(range(1,len(all_prices)+1)) #adding 1 extra index to compensate for starting range at 1
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

	# Grouped context data
	insight_stats = {
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

	location_address = ''
	# Ajax call filter sent each time the map is panned or zoomed by user
	if request.method == 'POST':
		# Request.post values are always bundled in every post request from the client
		# so that we have a consisent order on how items are being filtered or sorted
		def checkAllValue(param):
			return param == 'All';

		filtrer_params_dict = {}
		formdata = json.loads(request.POST.get('filterFormData'))
		for field in formdata:
			filtrer_params_dict[field["name"]] = field["value"]

		location = filtrer_params_dict['location']
		min_price = filtrer_params_dict['min_price']
		max_price = filtrer_params_dict['max_price']
		property_type= filtrer_params_dict['property_type']
		bedrooms = filtrer_params_dict['bedrooms']
		bathrooms = filtrer_params_dict['bathrooms']

		page = request.POST.get('page')
		print(page)
		sortValue = str(request.POST.get('sort'))
		array_of_pks = request.POST.getlist('pk_array[]')
		array_of_pks = list(map(int, array_of_pks))

		if check_q_valid(location):
			listings = listings.filter(location_name__icontains = str(location.split(',')[0]))
			location_address = location
		else:
			listings = listings.filter(location_name__icontains= 'Nairobi')
			location_address = 'Nairobi,Kenya'
		if check_q_valid(min_price) and check_q_valid(max_price):
			if checkAllValue(max_price): #if max price is set to all.
				max_price =  listings.aggregate(Max('price'))
				listings = listings.filter(price__range = (min_price,max_price['price__max']))
			else:
				listings = listings.filter(price__range = (min_price,max_price))
		if check_q_valid(property_type):
			if not checkAllValue(property_type):
				listings = listings.filter(type__iexact=property_type)
		if check_q_valid(bedrooms):
			#filter with beds submitted by user
			listings = listings.filter(bedrooms__gte=bedrooms)

			#finding n-median price for a n-bedroomed house to populate the template's insights bar
			n_bds_median_price = 0
			if listings:
				n_bds_prices = listings.values_list('price', flat=True).distinct()
				n_bds_median_price = statistics.median(n_bds_prices)
		if check_q_valid(bathrooms):
			listings = listings.filter(bathrooms__gte=bathrooms)

		listings = listings.filter(id__in = array_of_pks)

		#default sort with our chosen params
		if sortValue == 'jfy':
			listings = listings.order_by('-publishdate', 'price')
		#descending sort
		elif sortValue == 'newer':
			listings = listings.order_by('-publishdate')
		elif sortValue == 'pricehl':
			listings = listings.order_by('-price')
		#ascending sort
		elif sortValue == 'older':
			listings = listings.order_by('publishdate')
		elif sortValue == 'pricelh':
			listings = listings.order_by('price')
		elif sortValue == 'beds':
			listings = listings.order_by('bedrooms')
		elif sortValue == 'baths':
			listings = listings.order_by('bathrooms')
		elif sortValue == 'sqft':
			listings = listings.order_by('floor_area')
		else:
			listings = listings.order_by('-publishdate')

		filter_fields = {
			"min_price":min_price,
			"max_price":max_price,
			"property_type":property_type,
			"bedrooms":bedrooms,
			"bathrooms":bathrooms,
		}

		listings_count = listings.count()
		all_listings = listings
		# Main pagination
		# Used for all subsequent requests after the innitial page load
		paginator = Paginator(listings, 20)
		listings = paginator.get_page(page)
		return render(request, 'listings/property-listing-page.html', {
				"all_listings":all_listings,'listings':listings, 'listings_count':listings_count,
				"ImageTransformation":ImageTransformation ,"location_address":location_address,
				"insight_stats":insight_stats,"filter_fields":filter_fields
					})
	else:
		loc_input_q_get = request.GET.get('location')
		if check_q_valid(loc_input_q_get):
			loc_input_q_get = loc_input_q_get.split(',')[0]
			listings = listings.filter(location_name__icontains = str(loc_input_q_get))
			location_address = loc_input_q_get
		else:
			listings = listings.filter(location_name__icontains= 'Nairobi')
			location_address = 'Nairobi,Kenya'
		# Innitial pagination on page load
		# Used only when the page laods the first time
		listings_count = listings.count()
		all_listings = listings
		paginator = Paginator(listings, 20)
		page = request.GET.get('page')
		listings = paginator.get_page(page)

		return render(request, 'listings/property-listing-page.html', {
			"all_listings":all_listings,'listings':listings, 'listings_count':listings_count,
			"location_address":location_address, "ImageTransformation":ImageTransformation ,
			"insight_stats":insight_stats,
			})

# @login_required(login_url='account_login')
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

	is_saved = False
	if listing.saves.filter(id=request.user.id).exists():
		is_saved = True

	# filter for similar listings
	similar_listings = model_object.objects.filter(	\
		price__range = (listing.price - listing.price * 0.2, listing.price + listing.price * 0.2),
		location_name__icontains = listing.location_name.split(',')[0]
		).exclude(id = listing.id)
	similar_listings_in_area = model_object.objects.filter(	\
		price__range = (listing.price - listing.price * 0.2, listing.price + listing.price * 0.2),
		location_name__icontains = listing.location_name.split(',')[-1]
		).exclude(id = listing.id)

	return render(request, 'listings/property_detail_page.html', {'listing': listing,'is_saved':is_saved ,'images':images, 'videos': video,
				"similar_listings":similar_listings,"similar_listings_in_area":similar_listings_in_area,
				'ImageTransformation':ImageTransformation, 'VideoTransformation':VideoTransformation})

@login_required(login_url='account_login')
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
			return JsonResponse({'form':html, 'is_saved':is_saved})
	else:
		messages.error(request, 'Invalid Request!')
		return redirect('listings:homepage')

@login_required(login_url='account_login')
def property_listing_form(request):
	if request.user.user_type =='Agent' or request.user.user_type =='PropertyManager':
		if request.method =='POST':
				PropertyForm = forms.ListingForm(request.POST, request.FILES)
				ImageForm = forms.PhotoForm(request.POST, request.FILES)
				images = request.FILES.getlist('photo')#name of field
				VideoForm = forms.VideoForm(request.POST, request.FILES)
				videos = request.FILES.getlist('video')#name of field
				# Authenticate form
				if PropertyForm.is_valid() and PhotoForm.is_valid() and VideoForm.is_valid():
					instance = PropertyForm.save(commit=False)
					# Associate listing with user
					instance.owner = request.user
					# finally save to db
					instance.save()

					for img in images:
						file_instance = PropertyPhoto(photo = img, home = models.Home.objects.get(id=instance.id))
						file_instance.save()

					for vid in videos:
						file_instance2 = PropertyVideo(video = vid, home = models.Home.objectsget(id=instance.id))
						file_instance2.save()
					messages.success(request, 'Your Listing has been posted Successfully!')
					return redirect('profiles:account')
				else:
					messages.error(request,'Could not complete request. Try again later.')
		else:
			PropertyForm = forms.ListingForm()
			ImageForm = forms.PhotoForm()
			VideoForm = forms.VideoForm()
	else:
		messages.error(request,'Restricted. Your account type is not allowed to access this service.')
		return redirect('profiles:account')
	return render(request, 'listings/property_listing_form.html.html', {'PropertyForm': PropertyForm, 'ImageForm': ImageForm, 'VideoForm':VideoForm,})

@login_required(login_url='account_login')
def property_update(request, pk):
	model_object = ''
	if property_category == 'homes':
		model_object = models.Home
	else:
		messages.error(request, 'The path you requested is invalid!')
		return redirect('listings:homepage')

	listing = get_object_or_404(model_object, pk=pk)
	image_formset = modelformset_factory(PropertyForSaleImages, max_num=1, min_num=1, fields=('image',))
	video_formset = modelformset_factory(PropertyForSaleVideos, max_num=1, min_num=1, fields=('video',))
	if request.user == listing.owner:
		if request.method=='POST':
			PropertyForm = forms.ListingForm(request.POST, request.FILES, instance=listing)
			img_formset = image_formset(request.POST or None, request.FILES or None)
			vid_formset = video_formset(request.POST or None, request.FILES or None)
			if PropertyForm.is_valid() and img_formset.is_valid() and vid_formset.is_valid():
				listing = PropertyForm.save(commit=False)
				# Associate listing with user
				listing.owner = request.user
				# finally save to db
				listing.save()

				i_data = PropertyForSaleImages.objects.filter(property=listing)
				v_data = PropertyForSaleVideos.objects.filter(property=listing)

				for index, i in enumerate(img_formset):
					if i.cleaned_data:
						if i.cleaned_data['id'] is None:
							img = PropertyForSaleImages(property=listing, image=i.cleaned_data.get('image'))
							img.save()
						# elif i.cleaned_data['image'] is False:
						# 	img = PropertyForSaleImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	img.delete()
						else:
							img = PropertyForSaleImages(property=listing, image=i.cleaned_data.get('image'))
							p = PropertyForSaleImages.objects.get(id=i_data[index].id)
							p.image = img.image
							p.save()

				for index, v in enumerate(vid_formset):
					if v.cleaned_data:
						if v.cleaned_data['id'] is None:
							vid = PropertyForSaleVideos(property=listing, video=v.cleaned_data.get('video'))
							vid.save()
						# elif v.cleaned_data['video'] is False:
						# 	vid = PropertyForSaleVideos.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	vid.delete()
						else:
							vid = PropertyForSaleVideos(property=listing, video=v.cleaned_data.get('video'))
							p = PropertyForSaleVideos.objects.get(id=v_data[index].id)
							p.video = vid.video
							p.save()
				messages.success(request, 'Update Successull')
				return redirect('profiles:account')
			else:
				messages.error(request, 'Unable to update try again later')
		else:
			PropertyForm = forms.ListingForm(instance=listing)
			img_formset = image_formset(queryset = PropertyForSaleImages.objects.filter(property=listing))
			vid_formset = video_formset(queryset = PropertyForSaleVideos.objects.filter(property=listing))
	else:
		raise PermissionDenied
	return render(request, 'listings/update_form.html', {'PropertyForm':PropertyForm, 'listing':listing, 'img_formset':img_formset, 'vid_formset':vid_formset})

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
		return redirect('profiles:account')
	else:
		raise PermissionDenied
		return redirect('profiles:account')
