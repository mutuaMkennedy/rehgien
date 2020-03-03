from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib import messages
from . models import (
				PropertyForSale, PropertyForSaleImages,
				PropertyForSaleVideos, RentalProperty,RentalImages, RentalVideos,
				)
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import (
			ImageForm, VideoForm,
			RentalImageForm, RentalVideoForm,
			)
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
#from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
#from haystack.query import SearchQuerySet
# Create your views here.

# def directions(request):
# 	return render (request,"listings/navigation_map.html")

def homepage(request):
	onsale_recent = PropertyForSale.objects.order_by('publishdate')[:6]
	onsale_reversed = reversed(onsale_recent)
	#rentals
	rentals_recent = RentalProperty.objects.order_by('publishdate')[:6]
	rentals_reversed = reversed(rentals_recent)
	return render(request, 'listings/homey.html', {'onsale_reversed': onsale_reversed, 'rentals_reversed': rentals_reversed})

def onsale_detail(request, listing_id):
	listing = get_object_or_404(PropertyForSale, pk=listing_id)
	images = listing.images.all()
	videos = listing.videos.all()
	category = listing.categories.all()
	return render(request, 'listings/onsale_detail.html', {'listing': listing, 'images':images, 'videos': videos, 'category':category})

def rental_detail(request, listing_id):
	rentals = get_object_or_404(RentalProperty, pk=listing_id)
	images = rentals.images.all()
	videos = rentals.videos.all()
	return render(request, 'listings/rental_detail.html', {'rentals': rentals, 'images':images, 'videos': videos})

@login_required(login_url='account_login')
def listing_form(request):
	if request.method =='POST':
		PropertyForm = forms.ListingForm(request.POST, request.FILES)
		ImageForm = forms.ImageForm(request.POST, request.FILES)
		images = request.FILES.getlist('image')#name of field
		VideoForm = forms.VideoForm(request.POST, request.FILES)
		videos = request.FILES.getlist('video')#name of field
		# Authenticate form
		if PropertyForm.is_valid() and ImageForm.is_valid() and VideoForm.is_valid():
			instance = PropertyForm.save(commit=False)
			# Associate listing with user
			instance.owner = request.user
			# finally save to db
			instance.save()

			for img in images:
				file_instance = PropertyForSaleImages(image = img)
				file_instance.save()

			for vid in videos:
				file_instance2 = PropertyForSaleVideos(video = vid)
				file_instance2.save()
			messages.success(request, 'Your Listing has been posted Successfully!')
			return redirect('listings:homepage')
		else:
			messages.error(request,'Could not complete request!')
	else:
		PropertyForm = forms.ListingForm()
		ImageForm = forms.ImageForm()
		VideoForm = forms.VideoForm()
	return render(request, 'listings/sell-listing-form.html', {'PropertyForm': PropertyForm, 'ImageForm': ImageForm, 'VideoForm':VideoForm,})

@login_required(login_url='account_login')
def for_sale_update(request, pk):
	listing = get_object_or_404(PropertyForSale, pk=pk)
	#images = get_object_or_404(PropertyForSaleImages, pk=pk)
	#videos = get_object_or_404(PropertyForSaleVideos, pk=pk)
	if request.user == listing.owner:
		if request.method=='POST':
			PropertyForm = forms.ListingForm(request.POST, request.FILES, instance=listing)
			ImageForm = forms.ImageForm(request.POST, request.Files, instance=listing)
			images = request.FILES.getlist('image')#name of field
			VideoForm = forms.VideoForm(request.POST, request.Files,instance=listing)
			videos = request.FILES.getlist('video')#name of field
			if PropertyForm.is_valid() and ImageForm.is_valid() and VideoForm.is_valid():
				listing = PropertyForm.save(commit=False)
				# Associate listing with user
				listing.owner = request.user
				# finally save to db
				listing.save()

				for f in files:
					file_instance = PropertyForSaleImages(file = f, feed = listing)
					file_instance.save()

				for v in files:
					file_instance2 = PropertyForSaleVideos(file = v, feed = listing)
					file_instance2.save()

				messages.success(request, 'Update Successull')
				return HttpResponseRedirect(listing.get_absolute_url())
			else:
				messages.error(request, 'Ooops! Cannot Update Contact the adminstrator!!')
		else:
			PropertyForm = forms.ListingForm(instance=listing)
			ImageForm = forms.ImageForm(instance=listing)
			VideoForm = forms.VideoForm(instance=listing)
	else:
		raise PermissionDenied
	return render(request, 'listings/update_form.html', {'PropertyForm':PropertyForm, 'listing':listing, 'ImageForm':ImageForm, 'VideoForm':VideoForm})

@login_required(login_url='account_login')
def rental_listing_form(request):
	if request.method =='POST':
		PropertyForm = forms.RentalListingForm(request.POST, request.FILES)
		ImageForm = forms.RentalImageForm(request.POST, request.FILES)
		images = request.FILES.getlist('image')#name of field
		VideoForm = forms.RentalVideoForm(request.POST, request.FILES)
		videos = request.FILES.getlist('video')#name of field
		# Authenticate form
		if PropertyForm.is_valid() and ImageForm.is_valid() and VideoForm.is_valid():
			instance = PropertyForm.save(commit=False)
			# Associate listing with user
			instance.owner = request.user
			# finally save to db
			instance.save()

			for f in files:
				file_instance = RentalImages(file = f, feed = instance)
				file_instance.save()

			for v in files:
				file_instance2 = RentalVideos(file = v, feed = instance)
				file_instance2.save()
			messages.success(request, 'Your Listing has been posted Successfully!')
			return redirect('listings:homepage')
		else:
			messages.error(request,'Could not complete request!')
	else:
		PropertyForm = forms.RentalListingForm()
		ImageForm = forms.RentalImageForm()
		VideoForm = forms.RentalVideoForm()
	return render(request, 'listings/rent-listing-form.html', {'PropertyForm': PropertyForm, 'ImageForm': ImageForm, 'VideoForm':VideoForm,})


@login_required(login_url='account_login')
def for_rent_update(request, pk):
	listing = get_object_or_404(RentalProperty, pk=pk)
	#images = get_object_or_404(PropertyForSaleImages, pk=pk)
	#videos = get_object_or_404(PropertyForSaleVideos, pk=pk)
	if request.user == listing.owner:
		if request.method=='POST':
			PropertyForm = forms.RentalListingForm(request.POST, request.FILES, instance=listing)
			ImageForm = forms.RentalImageForm(request.POST, request.Files, instance=listing)
			images = request.FILES.getlist('image')#name of field
			VideoForm = forms.RentalVideoForm(request.POST, request.Files,instance=listing)
			videos = request.FILES.getlist('video')#name of field
			if PropertyForm.is_valid() and ImageForm.is_valid() and VideoForm.is_valid():
				listing = PropertyForm.save(commit=False)
				# Associate listing with user
				listing.owner = request.user
				# finally save to db
				listing.save()

				for f in files:
					file_instance = RentalImages(file = f, feed = listing)
					file_instance.save()

				for v in files:
					file_instance2 = RentalVideos(file = v, feed = listing)
					file_instance2.save()

				messages.success(request, 'Update Successull')
				return HttpResponseRedirect(listing.get_absolute_url())
			else:
				messages.error(request, 'Ooops! Cannot Update Contact the adminstrator!!')
		else:
			PropertyForm = forms.RentalListingForm(instance=listing)
			ImageForm = forms.RentalImageForm(instance=listing)
			VideoForm = forms.RentalVideoForm(instance=listing)
	else:
		raise PermissionDenied
	return render(request, 'listings/rental_update_form.html', {'PropertyForm':PropertyForm, 'listing':listing, 'ImageForm':ImageForm, 'VideoForm':VideoForm})

@login_required(login_url='account_login')
def delete_listing(request, pk):
	listing = get_object_or_404(PropertyForSale, pk=pk)
	if request.user == listing.owner:
		listing.delete()
		messages.success(request, 'Successfully deleted!!')
		return redirect('listings:homepage')
	else:
		raise PermissionDenied
		return redirect('listings:homepage')

@login_required(login_url = 'account_login')
@require_POST
def sale_like(request):
	if request.method == 'POST':
		user = request.user
		slug = request.POST.get('slug', None)
		property_for_sale = get_object_or_404(PropertyForSale, slug = slug)

		if property_for_sale.likes.filter(id=user.id).exists():
			#user has liked so remove like/user
			property_for_sale.likes.remove(user)
			messages = 'Saved item removed'
		else:
			#add the new like
			property_for_sale.likes.add(user)
			message = 'Save successfull!'

	context = {'likes_count': property_for_sale.totallikes, 'message': message}
	return HttpResponse(json.dumps(context), content_type = 'application/json')


#search views for haystack
#def autocomplete(request):
    #sqs = SearchQuerySet().autocomplete(
        #content_auto=request.GET.get(
            #'query',
            #''))[
        #:5]
    #s = []
    #for result in sqs:
        #d = {"value": result.name, "data": result.object.pk}
        #s.append(d)
    #output = {'suggestions': s}
    #return JsonResponse(output)

"""
class FacetedSearchView(BaseFacetedSearchView):

    form_class = FacetedSaleSearchForm
    facet_fields = ['location_name', 'type', 'bathrooms', 'bedrooms']
    template_name = 'search-results.html'
    paginate_by = 3
    context_object_name = 'object_list'

def rental_results(request):
	query = str(request.GET.get('q'))
	sqs = SearchQuerySet().filter(content=query).models(RentalProperty)
	return render(request, 'rental_search_results.html', {'sqs':sqs})
"""
