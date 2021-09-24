import africastalking

sms = africastalking.SMS

def send_otp_sms(otp_code):
    # Set the numbers in international format
    recipients = ["+254717966627","0746424465"]
    # Set your message
    message = "Your phone verification code is: {otp}".format(otp=otp_code);
    # Set your shortCode or senderId
    sender = "Rehgien"
    try:
        response = sms.send(message, recipients, sender)
        # print(response)
        return True
    except Exception as e:
        return({'status': False, 'detail': f'OTP code not sent: {e}'})
