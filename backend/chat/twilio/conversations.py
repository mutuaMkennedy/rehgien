from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from twilio.rest import Client
import json
import asyncio

User = get_user_model()

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
conversation_sid = settings.TWILIO_CONVERSATIONS_SERVICE_SID
api_key = settings.TWILIO_API_KEY
api_secret = settings.TWILIO_API_SECRET

# Innitialize the client
client = Client(account_sid, auth_token)
configuration = client.conversations \
                      .services(conversation_sid) \
                      .configuration() \
                      .update(reachability_enabled=True)


def createOrupdateUser(identity):
    """
    Helper function that will handle creating and updating the user's object on twilio
    """
    # Getting user info from our db and adding it to the user's account on twilio so we can use it from the chat frontend
    user_obj = User.objects.get(pk=identity)

    user_info = {
        "pk":user_obj.pk,
        "username":user_obj.username,
        "full_name":user_obj.get_full_name(),
        "user_type":user_obj.user_type,
        "has_profile_image":True if user_obj.profile_image else False,
        "profile_image":user_obj.profile_image.url if user_obj.profile_image else '/static/img/avatar_d2.svg',
        "business_name":user_obj.pro_business_profile.business_name if user_obj.user_type =='PRO' else '',
        "pro_category": user_obj.pro_business_profile.professional_category.category_name if user_obj.user_type =='PRO' else ''
        }

    twilio_user =''
    try:
        #  Update the user's atrributes if user exists
        twilio_user = client.conversations.services(conversation_sid).users(sid=identity).fetch()
        # We will need to specify the conversation service id because we have sid's for dev, pro and staging envs
        twilio_user = client.conversations \
             .services(conversation_sid) \
             .users(sid=str(identity)) \
             .update(
                  friendly_name=user_obj.username,
                  attributes=json.dumps(user_info)
              )

    except:
        # Register the user on twilio
        twilio_user = client.conversations.services(conversation_sid).users\
             .create(
                  identity=user_obj.pk,
                  friendly_name=user_obj.username,
                  attributes=json.dumps(user_info)
              )
    return twilio_user

def get_token(identity):
    # Make sure the user exists on twilio before trying to get token
    twilio_user = createOrupdateUser(identity)

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create an Chat grant and add to token
    chat_grant = ChatGrant(service_sid=conversation_sid)

    token.add_grant(chat_grant)

    return token.to_jwt()

def deleteConversation(conversationResourceSID):
    response=''
    try:
        client.conversations.services(conversation_sid) \
                        .conversations(conversationResourceSID) \
                        .delete();
        response = True
    except Exception as e:
        print(e)
        response = False

    return response
