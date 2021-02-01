import os
import io
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import get_user_model
from . import models
from . import profile_edit_forms as forms


# referencing the custom user model
User = get_user_model()
weekdays = [{'day': 1},{'day': 2},{'day': 3},{'day': 4},{'day': 5},{'day': 6},{'day': 7}]

@login_required(login_url='account_login')
def business_page_editor_mode(request, pk):
	bs_profile = get_object_or_404( models.BusinessProfile, pk=pk )
	bs_client_iformset = inlineformset_factory(
				models.BusinessProfile, models.Client, forms.ClientForm,
				min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
				exclude=('created_by','created_at')
				)

	bs_business_hours_iformset = inlineformset_factory(
				models.BusinessProfile, models.BusinessHours, forms.BusinessHoursForm,
				min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
				)
	user = request.user
	if user == bs_profile.user:
		profile_image_form= forms.BusinessProfileImage(instance=user.pro_business_profile)
		page_info_form= forms.BusinessProfilePageInfo(instance=user.pro_business_profile)
		about_form = forms.BusinessProfileAbout(instance=user.pro_business_profile)
		services_form = forms.BusinessProfileServices(instance=user.pro_business_profile)
		service_areas_form = forms.BusinessProfileServiceAreas(instance=user.pro_business_profile)

		bs_client_formset = bs_client_iformset(instance=bs_profile)
		bs_hours_formset = bs_business_hours_iformset(instance=bs_profile)

		all_connections = models.TeammateConnection.objects.all()
		pro_teammates = all_connections.filter(Q(requestor=bs_profile.user,receiver_accepted = 'No')|Q(receiver = bs_profile.user,receiver_accepted = 'No'))

		pro_reviews = bs_profile.pro_business_review.all()
		pro_reviews_count = pro_reviews.count()
		return render(request, 'profiles/editor_mode_files/business_page_update.html', {'bs_profile':bs_profile,
					'pro_reviews':pro_reviews,'pro_reviews_count':pro_reviews_count,
					'pro_teammates':pro_teammates,
					"profile_image_form":profile_image_form,
					"page_info_form":page_info_form,"about_form":about_form,
					"services_form":services_form,"service_areas_form":service_areas_form,
					"bs_client_formset":bs_client_formset,"bs_hours_formset":bs_hours_formset
					 })
	else:
		messages.error(request, 'Permission denied!')
		return redirect('profiles:account')

def resizePhoto(photo,x,y,width,height):
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

@login_required(login_url='account_login')
def busines_profile_update(request, pk, slug):
	if request.is_ajax() and request.method == 'POST':
		bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )
		if slug == 'profile-picture':
			profile_image_form = forms.BusinessProfileImage(request.POST, request.FILES, instance=request.user.pro_business_profile)

			if profile_image_form.is_valid():
				if request.user == bs_profile.user:
					instance = profile_image_form.save(commit=False)

					temp_photo = profile_image_form.cleaned_data['business_profile_image']
					x = profile_image_form.cleaned_data.get('x')
					y = profile_image_form.cleaned_data.get('y')
					w = profile_image_form.cleaned_data.get('width')
					h = profile_image_form.cleaned_data.get('height')

					cropped_photo = resizePhoto(temp_photo,x,y,w,h)

					instance.business_profile_image = cropped_photo
					instance.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'profile_image_form':profile_image_form
					}

					html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'profile_image_form':profile_image_form
					}

					html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'profile_image_form':profile_image_form
					}
				html = render_to_string('profiles/editor_mode_files/page_profile_image.html', context, request=request)
				return JsonResponse({'page_section':html ,'message':message})

		elif slug == 'service-areas':
			service_areas_form = forms.BusinessProfileServiceAreas(request.POST, instance=request.user.pro_business_profile)

			if service_areas_form.is_valid():
				if request.user == bs_profile.user:
					service_areas_form.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'service_areas_form':service_areas_form
					}

					html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'service_areas_form':service_areas_form
					}

					html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'service_areas_form':service_areas_form
					}
				html = render_to_string('profiles/editor_mode_files/service_areas.html', context, request=request)
				return JsonResponse({'page_section':html ,'message':message})
		elif slug == 'our-services':
			services_form = forms.BusinessProfileServices(request.POST, instance=request.user.pro_business_profile)

			if services_form.is_valid():
				if request.user == bs_profile.user:
					services_form.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'services_form':services_form
					}

					html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})
				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'services_form':services_form
					}

					html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'services_form':services_form
					}
				html = render_to_string('profiles/editor_mode_files/services.html', context, request=request)
				return JsonResponse({'page_section':html ,'message':message})
		elif slug == 'about-us':
			about_form = forms.BusinessProfileAbout(request.POST, request.FILES, instance=request.user.pro_business_profile)
			if about_form.is_valid():
				if request.user == bs_profile.user:
					about_form.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'about_form':about_form
					}

					html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})
				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'about_form':about_form
					}

					html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'about_form':about_form
					}
				html = render_to_string('profiles/editor_mode_files/about.html', context, request=request)
				return JsonResponse({'page_section':html ,'message':message})
		elif slug == 'page-info':
			page_info_form = forms.BusinessProfilePageInfo(request.POST, request.FILES, instance=request.user.pro_business_profile)
			bs_business_hours_iformset = inlineformset_factory(
						models.BusinessProfile, models.BusinessHours, forms.BusinessHoursForm,
						min_num=1,max_num=14, extra=0, can_order=True, can_delete=True
						)
			bs_hours_formset = bs_business_hours_iformset(request.POST, request.FILES, instance=bs_profile)

			if page_info_form.is_valid() and bs_hours_formset.is_valid():
				if request.user == bs_profile.user:
					page_info_form.save()
					bs_hours_formset.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'page_info_form':page_info_form, "bs_hours_formset":bs_hours_formset
					}

					html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
					business_dtls_html = render_to_string('profiles/editor_mode_files/business_dtls.html', context, request=request)
					return JsonResponse({'page_section':html , 'business_dtls_html':business_dtls_html, 'message':message})
				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'page_info_form':page_info_form, "bs_hours_formset":bs_hours_formset
					}

					html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'page_info_form':page_info_form, "bs_hours_formset":bs_hours_formset
					}
				html = render_to_string('profiles/editor_mode_files/page_info.html', context, request=request)
				return JsonResponse({'page_info_section':html ,'message':message})
		elif slug == 'top-clients':
			bs_client_iformset = inlineformset_factory(
						models.BusinessProfile, models.Client, forms.ClientForm,
						min_num=1,max_num=5, extra=0, can_order=True, can_delete=True,
						exclude=('created_by','created_at')
						)
			bs_client_formset = bs_client_iformset(request.POST, request.FILES, instance=bs_profile)

			if bs_client_formset.is_valid():
				if request.user == bs_profile.user:
					bs_client_formset.save()

					#we request an updated instance of the model
					bs_profile = get_object_or_404(models.BusinessProfile, pk=pk )

					message = 'Changes saved successfully!'
					context = {
					'message':message,'bs_profile':bs_profile,'bs_client_formset':bs_client_formset
					}

					html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})
				else:
					message = 'Permission denied. Changes not saved'
					context = {
					'message':message,'bs_profile':bs_profile,'bs_client_formset':bs_client_formset
					}

					html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
					return JsonResponse({'page_section':html ,'message':message})

			else:
				message = 'Invalid form submission!'
				context = {
					'message':message,'bs_profile':bs_profile,'bs_client_formset':bs_client_formset
					}
				html = render_to_string('profiles/editor_mode_files/top_clients.html', context, request=request)
				return JsonResponse({'page_info_section':html ,'message':message})
		else:
			messages.error(request, 'Invalid form requested. Changes no saved')
			return redirect('profiles:account')
	else:
		messages.error(request, 'Invalid request. Changes no saved')
		return redirect('profiles:account')
