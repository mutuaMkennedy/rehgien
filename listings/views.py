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
	return render(request, 'listings/onsale_detail.html', {'listing': listing, 'images':images, 'videos': videos})

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
				file_instance = PropertyForSaleImages(image = img, property=PropertyForSale.objects.get(id=instance.id))
				file_instance.save()

			for vid in videos:
				file_instance2 = PropertyForSaleVideos(video = vid, property=PropertyForSale.objects.get(id=instance.id))
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
				messages.error(request, 'Ooops! Cannot Update Contact the adminstrator!!')
		else:
			PropertyForm = forms.ListingForm(instance=listing)
			img_formset = image_formset(queryset = PropertyForSaleImages.objects.filter(property=listing))
			vid_formset = video_formset(queryset = PropertyForSaleVideos.objects.filter(property=listing))
	else:
		raise PermissionDenied
	return render(request, 'listings/update_form.html', {'PropertyForm':PropertyForm, 'listing':listing, 'img_formset':img_formset, 'vid_formset':vid_formset})

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

			for img in images:
				file_instance = RentalImages(image = img, property=RentalProperty.objects.get(id=instance.id))
				file_instance.save()

			for vid in videos:
				file_instance = RentalVideos(video = vid, property=RentalProperty.objects.get(id=instance.id))
				file_instance.save()
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
	image_formset = modelformset_factory(RentalImages, max_num=1, min_num=1, fields=('image',))
	video_formset = modelformset_factory(RentalVideos, max_num=1, min_num=1, fields=('video',))
	if request.user == listing.owner:
		if request.method=='POST':
			PropertyForm = forms.RentalListingForm(request.POST, request.FILES, instance=listing)
			img_formset = image_formset(request.POST or None, request.FILES or None)
			vid_formset = video_formset(request.POST or None, request.FILES or None)
			if PropertyForm.is_valid() and img_formset.is_valid() and vid_formset.is_valid():
				listing = PropertyForm.save(commit=False)
				# Associate listing with user
				listing.owner = request.user
				# finally save to db
				listing.save()

				i_data = RentalImages.objects.filter(property=listing)
				v_data = RentalVideos.objects.filter(property=listing)

				for index, i in enumerate(img_formset):
					if i.cleaned_data:
						if i.cleaned_data['id'] is None:
							img = RentalImages(property=listing, image=i.cleaned_data.get('image'))
							img.save()
						# elif i.cleaned_data['image'] is False:
						# 	img = RentalImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	img.delete()
						else:
							img = RentalImages(property=listing, image=i.cleaned_data.get('image'))
							p = RentalImages.objects.get(id=i_data[index].id)
							p.image = img.image
							p.save()

				for index, v in enumerate(vid_formset):
					if v.cleaned_data:
						if v.cleaned_data['id'] is None:
							vid = RentalVideos(property=listing, video=v.cleaned_data.get('video'))
							vid.save()
						# elif v.cleaned_data['video'] is False:
						# 	vid = RentalVideos.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						# 	vid.delete()
						else:
							vid = RentalVideos(property=listing, video=v.cleaned_data.get('video'))
							p = RentalVideos.objects.get(id=v_data[index].id)
							p.video = vid.video
							p.save()
				messages.success(request, 'Update Successull')
				return redirect('profiles:account')
			else:
				messages.error(request, 'Ooops! Cannot Update Contact the adminstrator!!')
		else:
			PropertyForm = forms.ListingForm(instance=listing)
			img_formset = image_formset(queryset = RentalImages.objects.filter(property=listing))
			vid_formset = video_formset(queryset = RentalVideos.objects.filter(property=listing))
	else:
		raise PermissionDenied
	return render(request, 'listings/rental_update_form.html', {'PropertyForm':PropertyForm, 'listing':listing, 'img_formset':img_formset, 'vid_formset':vid_formset})

@login_required(login_url='account_login')
def for_sale_delete(request, pk):
	listing = get_object_or_404(PropertyForSale, pk=pk)
	if request.user == listing.owner:
		listing.delete()
		messages.success(request, 'Successfully deleted!!')
		return redirect('profiles:account')
	else:
		raise PermissionDenied
		return redirect('profiles:account')

@login_required(login_url='account_login')
def for_rent_delete(request, pk):
	listing = get_object_or_404(RentalProperty, pk=pk)
	if request.user == listing.owner:
		listing.delete()
		messages.success(request, 'Successfully deleted!!')
		return redirect('profiles:account')
	else:
		raise PermissionDenied
		return redirect('profiles:account')

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
