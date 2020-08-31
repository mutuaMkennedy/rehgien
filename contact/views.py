from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService


def about_us(request):
    pass

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
                    'listingLink':current_listing_path
                     }
            htmlMessage = render_to_string('contact/ListingLeadMessage.html', context)

            # send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
            message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email])
            message.attach_alternative(htmlMessage, "text/html")
            message.send()
        except BadHeaderError:
            messages.error(request, 'Something went wrong! Could not complete request. Try again later')
            return redirect(current_listing_path)
        # sending lead alert via instant sms
        twilio_service = TwilioService()

        formatted_message = build_message(sender_message, name, phone_number, from_email,current_listing_name, \
                            current_listing_location,current_listing_path)
        try:
            e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
            twilio_service.send_message(formatted_message, e_recepient_phone_number)
            messages.success(request, 'Message sent successfully. The agent will contact you as soon as they get your message')
            return redirect(current_listing_path)
        except TwilioRestException as e:
            print(e)
            messages.error(request,"Something went wrong! Could not complete request. Try again later")
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
                     }
            htmlMessage = render_to_string('contact/ProServicesLeadMessage.html', context)

            # send_mail(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email], fail_silently=False)
            message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepient_email])
            message.attach_alternative(htmlMessage, "text/html")
            message.send()
        except BadHeaderError:
            messages.error(request, 'Something went wrong! Could not complete request. Try again later')
            return redirect(current_path)
        # sending lead alert via instant sms
        twilio_service = TwilioService()

        formatted_message = build_pro_message(sender_message, sender_name, sender_phone_number, sender_email)
        try:
            e_recepient_phone_number = '+254' + recepient_phone_number[-9:]
            twilio_service.send_message(formatted_message, e_recepient_phone_number)
            messages.success(request, 'Message sent successfully. This pro will contact you as soon as they get your message')
            return redirect(current_path)
        except TwilioRestException as e:
            print(e)
            messages.error(request,"Something went wrong! Could not complete request. Try again later")
            return redirect(current_path)
    else:
        messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
        return redirect(current_path)

def share_listing(request):
    property_name = request.POST.get("e_sS_propertyName", '')
    property_Location = request.POST.get("e_sS_PropertyLocation", '')
    property_absoluteUrl = request.POST.get("e_sS_absoluteUrl", '')
    property_image = request.POST.get("e_sS_propertyImage", '')
    property_price = request.POST.get("e_sS_PropertyPrice", '')
    property_bathrooms = request.POST.get("e_sS_PropertyBathrooms", '')
    property_bedrooms = request.POST.get("e_sS_PropertyBedrooms", '')
    property_size= request.POST.get("e_sS_PropertySize", '')
    senderEmail = request.POST.get("e_sS_senderEmail", '')
    recepientEmail = request.POST.get("e_sS_recepientEmail", '')
    subject = senderEmail + " wants you to see this home"

    if property_name and property_Location and property_absoluteUrl and property_image and \
        senderEmail and recepientEmail and property_price and property_bathrooms and property_bedrooms and property_size:
        try:
            plainMessage =  senderEmail  + ' wants you to see this home' + '\n url: ' + property_absoluteUrl + \
                            "From \n" + 'The Rehgien Team'
            context = {
                    'propertyLocation': property_Location,
                    'propertyName':property_name,
                    'recepientEmail':recepientEmail,
                    'senderEmail':senderEmail,
                    'property_absoluteUrl':property_absoluteUrl,
                    "propertyImage":property_image,
                    "propertyPrice":property_price,
                    "propertyBathrooms":property_bathrooms,
                    "propertyBedrooms":property_bedrooms,
                    "propertySize":property_size
                     }
            htmlMessage = render_to_string('contact/share_home.html', context)

            message = EmailMultiAlternatives(subject,plainMessage,'Rehgien <mutuakennedy81@gmail.com>', [recepientEmail])
            message.attach_alternative(htmlMessage, "text/html")
            message.send()

            messages.success(request, 'Share successfull. We have sent an email to ' + recepientEmail)
            return redirect(property_absoluteUrl)
        except BadHeaderError:
            messages.error(request, 'Something went wrong! Could not complete request. Try again later')
            return redirect(property_absoluteUrl)

    else:
        messages.error(request,"Ooops! something went wrong. Make sure all fields are entered and valid.")
        return redirect(property_absoluteUrl)
