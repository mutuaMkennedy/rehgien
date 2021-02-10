from . import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from contact import models
from rest_framework.generics import (
									CreateAPIView,
									ListAPIView,
									RetrieveUpdateAPIView,
									RetrieveAPIView,
									DestroyAPIView
									)
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from twilio.base.exceptions import TwilioRestException
from contact.services.twilio_service import TwilioService
from listings import models as listings_models
from contact.views import build_message,build_pro_message
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json

# referencing the custom user model
User = get_user_model()

def check_valid(param):
	return param != '' and param is not None

@api_view(['POST'])
def contact_listing_agent(request):
	try:
		client_name = request.data['client_name']
		client_phone_number = request.data['client_phone_number']
		client_message = request.data['client_message']
		client_email = request.data['client_email']
		recepient_email = request.data['recepient_email']
		recepient_phone_number = request.data['recepient_phone_number']
		property_id = request.data['property_id']
		subject = "Rehgien Lead alert on Listing"
		domain = 'http://' + Site.objects.get_current().domain
		if check_valid(client_name) and check_valid(client_phone_number) \
			and check_valid(client_message) and check_valid(client_email) and \
			check_valid(recepient_email) and check_valid(recepient_phone_number) and \
			check_valid(property_id):

			try:
				home_object = get_object_or_404(listings_models.Home, pk=str(property_id) )
				property_name = home_object.property_name
				property_location = home_object.location_name
				link_to_property =  domain + home_object.get_absolute_url()
				try:
					plainMessage =  client_message  + '\nClient Details:' + '\n Name: ' + client_name + \
									'\n Phone number: ' + client_phone_number  + '\n Email: ' + client_email + \
									'\nListing Details:'+  '\n Name:' + property_name + \
									'\n Location:'+ property_location + '\n Link: ' + link_to_property
					context = {
							'message': client_message,
							'senderName':client_name,
							'PhoneNumber':client_phone_number,
							'senderEmail':client_email,
							'listingName':property_name ,
							'propertyLocation':property_location ,
							'listingLink':link_to_property,
							'domain':domain
							 }

					htmlMessage = render_to_string('contact/ListingLeadMessage.html', context)

					message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email])
					message.attach_alternative(htmlMessage, "text/html")
					message.send()

					# After a successfull send update the property's leads field with the user
					# we don't need this check but we will have it as a precaution. Object should already exist b4 the user reaches this part
					try:
						interaction = get_object_or_404(listings_models.PropertyInteraction, user=request.user)
						_views_count = interaction.views_count
						listings_models.PropertyInteraction.objects.filter(home=home_object, user=request.user)\
									.update( is_lead =  True )
					except ObjectDoesNotExist:
						interaction_obj = listings_models.PropertyInteraction.objects.create(
												home = home_object,
												user = request.user,
												is_lead =  True,
												has_viewed = True,
												views_count = 1
												)
						interaction_obj.save()

				except BadHeaderError:
					message = 'Something went wrong! Could not complete request. Try again later'
					return Response(message)
				# sending lead alert via instant sms
				twilio_service = TwilioService()

				formatted_message = build_message(client_message, client_name, client_phone_number, client_email, property_name, \
									property_location,link_to_property)
				try:
					e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
					twilio_service.send_message(formatted_message, e_recepient_phone_number)
				except TwilioRestException as e:
					message = 'SMS not sent. Make sure the phone number supplied is correct!'

				message = 'Message sent sucessfully. This agent will contact you soon.'
				return Response(message)

			except ObjectDoesNotExist:
				message = "Referenced property does not exist."
				return Response(message)
		else:
			message = 'Empty fields are not allowed.'
			return Response(message)

	except:
		context = {
		"client_name": ['This field is required'],
		"client_phone_number": ['This field is required'],
		"client_message": ['This field is required'],
		"client_email": ['This field is required'],
		"recepient_email": ['This field is required'],
		"recepient_phone_number": ['This field is required'],
		"property_id": ['This field is required'],
		}
		return Response(context)

@api_view(['POST'])
def contact_pro(request):
	try:
		client_name = request.data["client_name"]
		client_phone_number = request.data["client_phone_number"]
		client_message = request.data["client_message"]
		client_email = request.data["client_email"]
		recepient_email = request.data["recepient_email"]
		recepient_phone_number = request.data["recepient_phone_number"]
		subject = 'Rehgien Lead alert on professional services'
		domain = 'http://' + Site.objects.get_current().domain
		if check_valid(client_name) and check_valid(client_phone_number) \
			and check_valid(client_message) and check_valid(client_email) and \
			check_valid(recepient_email) and check_valid(recepient_phone_number):
			try:
				plainMessage =  client_message  + '\nSubmited user data' + '\n Name: ' + client_name + \
								'\n Phone number: ' + client_phone_number  + '\n Email: ' + client_email
				context = {
						'message': client_message,
						'senderName':client_name,
						'senderPhoneNumber':client_phone_number,
						'senderEmail':client_email,
						'domain':domain
						 }
				htmlMessage = render_to_string('contact/ProServicesLeadMessage.html', context)

				message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email])
				message.attach_alternative(htmlMessage, "text/html")
				message.send()
			except BadHeaderError:
				message = 'Something went wrong! Could not complete request. Try again later'
				return Response(message)

			# sending lead alert via instant sms
			twilio_service = TwilioService()
			formatted_message = build_pro_message(client_message, client_name, client_phone_number, client_email)
			try:
				e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
				twilio_service.send_message(formatted_message, e_recepient_phone_number)
			except TwilioRestException as e:
				message = 'SMS not sent. Make sure the phone number supplied is correct!'
			message = 'Message sent sucessfully. This agent will contact you soon.'
			return Response(message)
		else:
			message = 'Empty fields are not allowed.'
			return Response(message)
	except:
		context = {
		"client_name": ['This field is required'],
		"client_phone_number": ['This field is required'],
		"client_message": ['This field is required'],
		"client_email": ['This field is required'],
		"recepient_email": ['This field is required'],
		"recepient_phone_number": ['This field is required'],
		}
		return Response(context)

@api_view(['POST'])
def share_listing(request):
	try:
		property_id = request.data['property_id']
		sender_email = request.data['sender_email']
		recepient_email = request.data['recepient_email']
		domain = 'http://' + Site.objects.get_current().domain
		subject = sender_email + " wants you to see this home"
		ImageTransformation = dict(
			format = "jpg",
			transformation = [
				dict(height=333, width=500, crop="fill",quality="auto", gravity="center",
				 format="auto", dpr="auto", fl="progressive"),
					]
				)
		if check_valid(property_id) and check_valid(sender_email) and check_valid(recepient_email):
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
					plainMessage =  sender_email  + ' wants you to see this home' + '\n url: ' + link_to_property + \
									"From \n" + 'The Rehgien Team'
					context = {
							'propertyLocation': property_Location,
							'propertyName':property_name,
							'recepientEmail':recepient_email,
							'senderEmail':sender_email,
							'property_absoluteUrl':link_to_property,
							"propertyImage":property_image,
							"propertyPrice":property_price,
							"propertyBathrooms":property_bathrooms,
							"propertyBedrooms":property_bedrooms,
							"propertySize":property_size,
							"ImageTransformation":ImageTransformation
							 }
					htmlMessage = render_to_string('contact/share_home.html', context)

					message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email])
					message.attach_alternative(htmlMessage, "text/html")
					message.send()

					message = 'Share successfull. We have sent an email to ' + recepient_email
					return Response(message)
				except BadHeaderError:
					message = 'Something went wrong! Could not complete request. Try again later'
					return Response(message)
			except:
				message = 'We cannot find this property. Make sure it exists.'
				return Response(message)
		else:
			message = 'Ooops! something went wrong. Make sure all fields are entered and valid.'
			return Response(message)
	except:
		context = {
		"property_id":['This field is required'],
		"sender_email":['This field is required'],
		"recepient_email":['This field is required']
		}
		return Response(context)

class PageReportApi(CreateAPIView):
	queryset = models.PageReport.objects.all()
	serializer_class = serializers.PageReportSerializer
	permission_classes = [permissions.IsAuthenticated]

class PortfolioReportApi(CreateAPIView):
	queryset = models.ProjectsPortfolioReport.objects.all()
	serializer_class = serializers.PortfolioReportSerializer
	permission_classes = [permissions.IsAuthenticated]

class ReviewReportApi(CreateAPIView):
	queryset = models.ReviewReport.objects.all()
	serializer_class = serializers.ReviewReportSerializer
	permission_classes = [permissions.IsAuthenticated]
