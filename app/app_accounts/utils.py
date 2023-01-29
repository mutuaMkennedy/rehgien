import re
from contact.services import twilio_service
from django.contrib.auth import get_user_model
from profiles import models

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'^\+?1?\d{9,14}$'

def is_email(q):
    return re.fullmatch(email_regex, q)

def is_phone(q):
    return re.fullmatch(phone_regex,q)


"""
Validate new user phone number and handle otp requests
"""
def send_otp(phone_number,message):
    """
        Helper function for generating and sending otp code to user's phone.
    """

    if phone_number:
        otp_code = otp_generator()
        phone = str(phone_number)
        try:
            #send code to phone Number
            message = f'{message} {otp_code}'
            sms = twilio_service.send_SMS(message, phone)
            if sms == True:
                return str(otp_code) # that we will store in the db for later validation when the user sends the code for verification
            else:
                return False
        except Exception as e:
            print(e)
            return False

def check_otp_count(phone_number):
    old_otp = models.PhoneOTP.objects.filter(phone__exact = phone_number)
    if old_otp.exists():
        if old_otp.first().count > 7:
            message = {'status': False, 'detail': 'Maximum OTP code requests reached. Contact customer support.'}
            return message
        else:
            return True
    else:
        return True

def validate_phone_send_otp(phone):
    phone_number = phone
    #check if phone number exist in the request
    if phone_number:
        user_obj = User.objects.filter(phone__iexact = phone_number)
        if user_obj.exists(): #check if user exist
            return {'status': False, 'detail': 'User with that phone number already exists.'}
        else:
            otp_count_check_status = check_otp_count(phone_number)
            if otp_count_check_status == True: # if true, meaning check passed, continue with the rest of the program
                otp_code = send_otp(phone_number, 'You phone number verification code is:')
                if otp_code != False:
                    """
                    Checking whether otp code object exists before we create a new one.
                    If exists increase the count if not create the otp object
                    """
                    old_otp = ''
                    try:
                        old_otp = models.PhoneOTP.objects.get(phone__exact = phone_number)
                    except:
                        pass
                    if old_otp:
                        ins_count = old_otp.count
                        old_otp.count = ins_count + 1 # Increase the count
                        old_otp.otp = otp_code # Update the old otp with the new otp code
                        old_otp.save(update_fields=['count','otp'])
                    else:
                        models.PhoneOTP.objects.create(
                            phone = phone_number,
                            otp = otp_code,
                            count = 1
                        )

                    return {'status':True, 'detail': 'OTP code sent succesfully.'}
                else:
                    return {'status': False, 'detail':'OTP code not sent. Try again later.'}
            else: # Check failed and user has maxed out 7 otp requests allowed.
                return {'status': otp_count_check_status, 'detail':'Maximum OTP requests reached'}
    else:
        return {'status':False, 'detail':'Phone number is required e.g. +254xxxxxxxxx'}
