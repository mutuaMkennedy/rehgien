from twilio.rest import Client

class TwilioService:
    client = None

    def __init__(self):
        account_sid = 'AC1db0e8cfbae1e3b9b5834772c0ef8d6c'
        auth_token = '7f70419841a1632045d657089acd65c1'
        self.client = Client(account_sid, auth_token)

    def send_message(self, message):
        agent_phone_number = '+254717966627'
        twilio_phone_number = '+12054633293'
        self.client.messages.create(to=agent_phone_number,
                                    from_=twilio_phone_number,
                                    body=message)
