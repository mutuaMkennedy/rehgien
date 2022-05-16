# import africastalking

# sms = africastalking.SMS

# def send_otp_sms(otp_code):
#     # Set the numbers in international format
#     recipients = ["+254717966627","+254746424465"]
#     # Set your message
#     message = "Your phone verification code is: {otp}".format(otp=otp_code);
#     # Set your shortCode or senderId
#     sender = "3839"
#     try:
#         response = sms.send(message, recipients, sender)
#         # print(response)
#         return True
#     except Exception as e:
#         return({'status': False, 'detail': f'OTP code not sent: {e}'})

# def send_password_reset_otp_sms(otp_code):
#     # Set the numbers in international format
#     recipients = ["+254717966627","+254746424465"]
#     # Set your message
#     message = "Your password reset code is: {otp}".format(otp=otp_code);
#     # Set your shortCode or senderId
#     sender = "3839"
#     try:
#         response = sms.send(message, recipients, sender)
#         # print(response)
#         return True
#     except Exception as e:
#         return({'status': False, 'detail': f'OTP code not sent: {e}'})
