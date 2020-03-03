from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def send_email(request):
    name = request.POST.get('name', '')
    phone_number = request.POST.get('phone_number', '')
    subject = 'Im interested with your Listing'
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    #recepient = request.POST.get('recepient', '')
    if name and phone_number and  subject and message and from_email:
        try:
            send_mail(subject, message + ' [ ' + 'Client Name:' + ' ' + name + ' | ' + 'Phone number: ' + phone_number + ' | ' + 'Email: ' + from_email + ' ] ' ,
            from_email, ["mutuakennedy81@gmail.com"], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponse("Thank You! The agent will contact you as soon as they get your message.")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Ooops! something is wrong. Make sure all fields are entered and valid.')

def about_us(request):
    return render(request, "contact/about_us.html")
