from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from twilio.base.exceptions import TwilioRestException
from .services import twilio_service
from . import models
from . import forms
from listings import models as listings_models
from profiles import models as profiles_models
from django.contrib.sites.models import Site
from django.urls import reverse
from . import utils


def contact_us(request):
	if request.method == 'POST':
		contact_form = forms.ContactUsForm(request.POST, request.FILES)
		if contact_form.is_valid():
			first_name = contact_form.cleaned_data.get('first_name')
			last_name = contact_form.cleaned_data.get('last_name')
			email = contact_form.cleaned_data.get('email')
			phone = contact_form.cleaned_data.get('phone')
			message = contact_form.cleaned_data.get('message')
			sucess = utils.contact_support(first_name, last_name, email, phone, message)

			if sucess:
				messages.success(request,"Message Sucessfully Sent!")
			else:
				messages.error(request,"Something went wrong try again later")
		else:
			messages.error(request,"Invalid submission. Check the form for field errors.")
	else:
		contact_form = forms.ContactUsForm()
	context = {'contactForm':contact_form}
	return render(request, 'contact/contact_us.html', context)


def about_us(request):
	context = {}
	return render(request,'contact/about_us.html', context)

# Listing message service
def build_message( message,name, phone_number, from_email, current_listing_name, current_listing_location, current_listing_path ):
	template = """ A new lead has been captured for your listing.\n
	 Message: {} \n
	 Submited user data \n
	 Client Name: {}\n
	 Phone Number: {}\n
	 Email: {}. \n
	 Property Data \n
	 Property Name: {} \n
	 Location Name: {} \n
	 Listing URL: {} """

	return template.format(message,name, phone_number, from_email, current_listing_name, current_listing_location, current_listing_path)

def build_pro_message(sender_message, sender_name, sender_phone_number, sender_email):
	template = """ A new lead has been captured from your business profile.\n
	 Message: {} \n
	 Submited user data \n
	 Client Name: {}\n
	 Phone Number: {}\n
	 Email: {}."""

	return template.format(sender_message, sender_name, sender_phone_number, sender_email)

def contact_listing_agent(request):
	propertyId = request.POST.get('listingID', '')

	name = request.POST.get('name', '')
	phone_number = request.POST.get('phone_number', '')
	subject = 'Rehgien Lead alert on Listing'
	sender_message = request.POST.get('message', '')
	from_email = request.POST.get('from_email', '')
	recepient_email = request.POST.get('recepient', '')
	recepient_phone_number = request.POST.get('recepientPhoneNumber','')
	current_listing_path = request.POST.get('currentListingPath', '')
	current_listing_name = request.POST.get('currentListingName', '')
	current_listing_location = request.POST.get('currentListingLocation', '')
	domain = 'http://' + Site.objects.get_current().domain
	if name and phone_number and  subject and sender_message and from_email:
		# sending lead alert via email
		try:
			plainMessage =  sender_message  + '\nClient Details:' + '\n Name: ' + name + \
							'\n Phone number: ' + phone_number  + '\n Email: ' + from_email + \
							'\nListing Details:'+  '\n Name:' + current_listing_name + \
							'\n Location:'+ current_listing_location + '\n Link: ' + current_listing_path
			context = {
					'message': sender_message,
					'senderName':name,
					'PhoneNumber':phone_number,
					'senderEmail':from_email,
					'listingName':current_listing_name,
					'propertyLocation':current_listing_location,
					'listingLink':current_listing_path,
					'domain':domain
					 }
			htmlMessage = render_to_string('contact/ListingLeadMessage.html', context)

			message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [recepient_email])
			message.attach_alternative(htmlMessage, "text/html")
			message.send()

			# After a successfull send update the property's leads field with the user
			home_object = get_object_or_404(listings_models.Home, pk=str(propertyId) )
			# we don't need this check but we will have it as a precaution. Object should already exist b4 the user reaches this part
			try:
				interaction = get_object_or_404(listings_models.PropertyInteraction,home=home_object, user=request.user)
				_views_count = interaction.views_count
				listings_models.PropertyInteraction.objects.filter(home=home_object, user=request.user)\
							.update( is_lead =  True )
			except:
				interaction_obj = listings_models.PropertyInteraction.objects.create(
										home = home_object,
										user = request.user,
										is_lead =  True,
										has_viewed = True,
										views_count = 1
										)
				interaction_obj.save()

		except BadHeaderError:
			messages.error(request, 'Something went wrong! Could not complete request. Try again later')
			return redirect(current_listing_path)
		# sending lead alert via instant sms

		formatted_message = build_message(sender_message, name, phone_number, from_email,current_listing_name, \
							current_listing_location,current_listing_path)
		try:
			e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
			twilio_service.send_SMS(formatted_message, e_recepient_phone_number)
		except TwilioRestException as e:
			pass

		messages.success(request,"Message sent successfully. The agent will contact you as soon as they get your message")
		return redirect(current_listing_path)

	else:
		messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
		return redirect(current_listing_path)

# Proffesional contact service

def contact_pro(request):
	sender_name = request.POST.get('name', '')
	sender_phone_number = request.POST.get('phone_number', '')
	subject = 'Rehgien Lead alert on professional services'
	sender_message = request.POST.get('message', '')
	sender_email = request.POST.get('from_email', '')
	recepient_email = request.POST.get('recepient', '')
	recepient_phone_number = request.POST.get('recepientPhoneNumber','')
	current_path = request.POST.get('currentPath', '')
	domain = 'http://' + Site.objects.get_current().domain
	if sender_name and sender_phone_number and  subject and sender_message and sender_email:
		# sending lead alert via email
		try:
			plainMessage =  sender_message  + '\nSubmited user data' + '\n Name: ' + sender_name + \
							'\n Phone number: ' + sender_phone_number  + '\n Email: ' + sender_email
			context = {
					'message': sender_message,
					'senderName':sender_name,
					'senderPhoneNumber':sender_phone_number,
					'senderEmail':sender_email,
					'domain':domain
					 }
			htmlMessage = render_to_string('contact/ProServicesLeadMessage.html', context)

			# send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
			message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [recepient_email])
			message.attach_alternative(htmlMessage, "text/html")
			message.send()
		except BadHeaderError:
			messages.error(request, 'Something went wrong! Could not complete request. Try again later')
			return redirect(current_path)
		# sending lead alert via instant sms
		formatted_message = build_pro_message(sender_message, sender_name, sender_phone_number, sender_email)
		try:
			e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
			twilio_service.send_SMS(formatted_message, e_recepient_phone_number)
		except TwilioRestException as e:
			pass

		messages.success(request,"Message sent successfully. This pro will contact you as soon as they get your message")
		return redirect(current_path)
	else:
		messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
		return redirect(current_path)

def share_listing(request):
	property_id = request.POST.get("e_sS_propertyID", '')
	senderEmail = request.POST.get("e_sS_senderEmail", '')
	recepientEmail = request.POST.get("e_sS_recepientEmail", '')
	request_path = request.POST.get("e_sS_requestPath", '')
	subject = senderEmail + " wants you to see this home"
	domain = 'http://' + Site.objects.get_current().domain
	ImageTransformation = dict(
		format = "jpg",
		transformation = [
			dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
			 format="auto", dpr="auto", fl="progressive"),
				]
			)

	if property_id and senderEmail and recepientEmail:
		try:
			home_object = get_object_or_404(listings_models.Home, pk=str(property_id) )

			property_name = home_object.property_name
			property_Location = home_object.location_name
			property_price = home_object.price
			property_bathrooms = home_object.bathrooms
			property_bedrooms = home_object.bedrooms
			property_size= home_object.floor_area
			link_to_property =  domain + home_object.get_absolute_url()
			property_image = home_object.home_photos.last()

			try:
				plainMessage =  senderEmail  + ' wants you to see this home' + '\n url: ' + link_to_property + \
								"From \n" + 'The Rehgien Team'
				context = {
						'propertyLocation': property_Location,
						'propertyName':property_name,
						'recepientEmail':recepientEmail,
						'senderEmail':senderEmail,
						'property_absoluteUrl':link_to_property,
						"propertyImage":property_image,
						"propertyPrice":property_price,
						"propertyBathrooms":property_bathrooms,
						"propertyBedrooms":property_bedrooms,
						"propertySize":property_size,
						"domain":domain
						 }
				htmlMessage = render_to_string('contact/share_home.html', context)

				message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [recepientEmail])
				message.attach_alternative(htmlMessage, "text/html")
				message.send()
				messages.success(request, 'Share successfull. We have sent an email to ' + recepientEmail)
				return redirect(request_path)

			except BadHeaderError:
				messages.error(request, 'Something went wrong! Could not complete request. Try again later')
				return redirect(request_path)

		except:
			messages.error(request, 'We cannot find this property. Make sure it exists.')
			return redirect(request_path)
	else:
		messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
		return redirect(request_path)

def request_team_connection(requestor_business_profile_pk, receiver_business_profile_pk):
	domain = 'http://' + Site.objects.get_current().domain
	if requestor_business_profile_pk and receiver_business_profile_pk:
		try:
			requestor_obj = get_object_or_404(profiles_models.BusinessProfile, pk=int(requestor_business_profile_pk))
			receiver_obj = get_object_or_404(profiles_models.BusinessProfile, pk=int(receiver_business_profile_pk))
			subject = "{rc_name}, please add me to your team".format(rc_name = receiver_obj.business_name)
			ImageTransformation = dict(
				format = "jpg",
				transformation = [
					dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
					 format="auto", dpr="auto", fl="progressive"),
						]
					)
			try:
				sender_message = "Hi {rc_name}, I'd like to join your team on Rehgien.".format(rc_name = receiver_obj.business_name)
				plainMessage = sender_message
				context = {
						'message': sender_message,
						'requestorProfileImage':requestor_obj.business_profile_image,
						'requestorName':requestor_obj.user.get_full_name() if requestor_obj.user.get_full_name() else requestor_obj.user.username,
						'requestorBusinessName':requestor_obj.business_name,
						'requestorBusinessPageLink':domain + requestor_obj.get_absolute_url(),
						'notificationsLink':domain + reverse('profiles:connection_request_action'),
						'domain':domain,
						"ImageTransformation":ImageTransformation
						 }
				htmlMessage = render_to_string('contact/join_team_request.html', context)

				# send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
				message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [receiver_obj.user.email])
				message.attach_alternative(htmlMessage, "text/html")
				message.send()
			except BadHeaderError:
				message = 'Something went wrong! Could not complete request. Try again later'
		except:
			raise
			# message = "Something went wrong could not find user!"
	else:
		message = 'Something went wrong! Could not complete request.'

def team_connection_request_acccepted(requestor_business_profile_pk, receiver_business_profile_pk):
	domain = 'http://' + Site.objects.get_current().domain
	if requestor_business_profile_pk and receiver_business_profile_pk:
		try:
			requestor_obj = get_object_or_404(profiles_models.BusinessProfile, pk=int(requestor_business_profile_pk))
			receiver_obj = get_object_or_404(profiles_models.BusinessProfile, pk=int(receiver_business_profile_pk))
			subject = "{rc_name}, accepted your connection request".format(rc_name = receiver_obj.business_name)
			ImageTransformation = dict(
				format = "jpg",
				transformation = [
					dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
					 format="auto", dpr="auto", fl="progressive"),
						]
					)
			try:
				sender_message = "{rc_name} has accepted your connection request. Your profiles are now visible on both of your business pages.".format(rc_name = receiver_obj.business_name)
				plainMessage = sender_message
				context = {
						'message': sender_message,
						'receiverProfileImage':receiver_obj.business_profile_image,
						'receiverName':receiver_obj.user.get_full_name() if receiver_obj.user.get_full_name() else receiver_obj.user.username,
						'receiverBusinessName':receiver_obj.business_name,
						'domain':domain,
						"ImageTransformation":ImageTransformation,
						"receiverBusinessPageLink":domain + receiver_obj.get_absolute_url()
						 }
				htmlMessage = render_to_string('contact/join_team_request_accepted.html', context)

				# send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
				message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <do-not-reply@rehgien.com>', [requestor_obj.user.email])
				message.attach_alternative(htmlMessage, "text/html")
				message.send()
			except BadHeaderError:
				message = 'Something went wrong! Could not complete request. Try again later'
		except:
			raise
			# message = "Something went wrong could not find user!"
	else:
		message = 'Something went wrong! Could not complete request.'

# Send email alerts to pros on their profile completion state

def send_pro_profile_completion_progress():
	domain = 'http://' + Site.objects.get_current().domain
	profiles = profiles_models.BusinessProfile.objects.all()
	for profile in profiles:
		important_fields = {
		'business_name':'False',
		'business_profile_image':'False',
		'phone':'False',
		'business_email':'False',
		'address':'False',
		'about':'False',
		}
		for field in important_fields:
			profile_field = profiles_models.BusinessProfile.objects.values_list(field, flat=True).get(pk=profile.pk)
			if profile_field:
				important_fields[field] = 'True'

		# These field are relationship filed and are checked and appended in separately
		# due to a problem that raised if the fields had many entries
		if profile.professional_category:
			important_fields['professional_category']= 'True'
		else:
			important_fields['professional_category']= 'False'
		if profile.service_areas:
			important_fields['service_areas']= 'True'
		else:
			important_fields['service_areas']= 'False'
		if profile.professional_services:
			important_fields['professional_services']= 'True'
		else:
			important_fields['professional_services']= 'False'

		# Send notification email to pro if one of the important steps is False
		nameTitle = profile.business_name if profile.business_name else "Your page"
		subject = "People may have a hard time finding {nT}.".format(nT = nameTitle)
		if 'False' in important_fields.values():
			try:
				title = "{nT} is missing some important information.".format(nT = nameTitle)
				message = "Without this information, people may have a harder time discovering and learning about your business. Add more info to {nT}, it will only take a minute or two.".format(nT = nameTitle)
				context = {
						'title':title,
						'message': message,
						'domain':domain,
						"edit_page_link":domain + reverse('profiles:pro_business_page_edit',kwargs={'pk':profile.pk}),
						"fields_list":important_fields
						 }
				htmlMessage = render_to_string('contact/complete_your_profile.html', context)

				message = EmailMultiAlternatives(subject,message,'Rehgien <do-not-reply@rehgien.com>', [profile.user.email])
				message.attach_alternative(htmlMessage, "text/html")
				message.send()
			except BadHeaderError:
				message = 'Something went wrong! Could not complete request. Try again later'


#Problem Reports

def check_valid(item):
	return item !=''

def page_report(request):
	if request.method == 'POST':
		subject_user_id = request.POST.get('rFo-Sub-user-pk')
		subject_page_url = request.POST.get('rFo-current-path')
		problem = request.POST.get('rFo-Problem')
		email = request.POST.get('rFo-Email')
		details = request.POST.get('rFo-Details')

		if check_valid(subject_user_id) and check_valid(subject_page_url) \
		and check_valid(problem) and check_valid(email):
			problem = models.PageReport.objects.create(
						problem = str(problem),
						email = email,
						details = str(details),
						subject_user_id = int(subject_user_id)
						)
			messages.success(request, 'Problem Submited. Thank you!')
			return redirect(subject_page_url)
		else:
			messages.success(request, 'Invalid entry. Try again later!')
			return redirect(subject_page_url)
	else:
		return redirect('listings:homepage')

def p_p_report(request):
	if request.method == 'POST':
		subject_user_id = request.POST.get('rFo-Sub-user-pk')
		subject_p_id = request.POST.get('rFo-Sub-project-pk')
		subject_page_url = request.POST.get('rFo-current-path')
		problem = request.POST.get('rFo-Problem')
		email = request.POST.get('rFo-Email')
		details = request.POST.get('rFo-Details')

		if check_valid(subject_user_id) and check_valid(subject_page_url) and check_valid(subject_p_id)\
		and check_valid(problem) and check_valid(email):
			problem = models.ProjectsPortfolioReport.objects.create(
						problem = str(problem),
						email = email,
						details = str(details),
						subject_user_id = int(subject_user_id),
						subject_item_id = int(subject_p_id)
						)
			messages.success(request, 'Problem Submited. Thank you!')
			return redirect(subject_page_url)
		else:
			messages.success(request, 'Invalid entry. Try again later!')
			return redirect(subject_page_url)
	else:
		return redirect('listings:homepage')

def review_report(request):
	if request.method == 'POST':
		subject_user_id = request.POST.get('rFo-Sub-user-pk')
		subject_item_id = request.POST.get('rFo-Sub-review-pk')
		subject_page_url = request.POST.get('rFo-current-path')
		problem = request.POST.get('rFo-Problem')
		email = request.POST.get('rFo-Email')
		details = request.POST.get('rFo-Details')

		if check_valid(subject_user_id) and check_valid(subject_page_url) and check_valid(subject_item_id)\
		and check_valid(problem) and check_valid(email):
			problem = models.ReviewReport.objects.create(
						problem = str(problem),
						email = email,
						details = str(details),
						subject_user_id = int(subject_user_id),
						subject_item_id = int(subject_item_id)
						)
			messages.success(request, 'Problem Submited. Thank you!')
			return redirect(subject_page_url)
		else:
			messages.success(request, 'Invalid entry. Try again later!')
			return redirect(subject_page_url)
	else:
		return redirect('listings:homepage')
