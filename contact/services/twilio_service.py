from django.conf import settings
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
messaging_sid = settings.TWILIO_MESSAGING_SERVICE_SID
twilio_phone_number = settings.TWILIO_PHONE_NUMBER

client = Client(account_sid, auth_token)

def send_SMS(message, recepient_phone_number):
    try:
        message = client.messages \
            .create(
                 body=message,
                 messaging_service_sid=messaging_sid,
                 to=recepient_phone_number
             )
        return True
    except Exception as e:
        return False
