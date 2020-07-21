from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService


def build_message( name, phone_number,from_email, message):
    template = 'New lead alert. Call {} at {} or email at {}. Message: {}'
    return template.format(name, phone_number, from_email,message)

def send_message(request):
    name = request.POST.get('name', '')
    phone_number = request.POST.get('phone_number', '')
    subject = 'Rehgien Lead alert on Listing'
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    #recepient = request.POST.get('recepient', '')
    if name and phone_number and  subject and message and from_email:
        # sending lead alert via email
        try:
            send_mail(subject, message + ' [ ' + 'Client Name:' + ' ' + name + ' | ' + 'Phone number: ' + phone_number + ' | ' + 'Email: ' + from_email + ' ] ' ,
            'Rehgien <mutuakennedy81@gmail.com>', ["mutuakennedy81@gmail.com"], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        # sending lead alert via instant sms
        twilio_service = TwilioService()

        formatted_message = build_message(name, phone_number, from_email, message)
        try:
            twilio_service.send_message(formatted_message)
            return HttpResponse("Thank You! The agent will contact you as soon as they get your message.")
        except TwilioRestException as e:
            print(e)
            return HttpResponse("Something went wrong! Could not complete request. Try again later")
    else:
        return HttpResponse('Ooops! something went wrong. Make sure all fields are entered and valid.')

def about_us(request):
    return render(request, "contact/about_us.html")
