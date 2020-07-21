from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from profiles.models import AgentProfile
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.core.serializers import serialize
import json
import stream_chat
# referencing the custom user model
User = get_user_model()

STREAM_KEY = settings.STREAM_API_KEY
STREAM_API_SECRET= settings.STREAM_API_SECRET

def chat_room(request):
    return render(request,'chat/chat_room.html')

def user_token(request):
    chat_client = stream_chat.StreamChat(api_key=STREAM_KEY, api_secret=STREAM_API_SECRET)
    token = chat_client.create_token(
                        request.user.username,
                        # exp=datetime.datetime.utcnow() + datetime.timedelta(hours=1)  #to be set in production
                    )
    # user_image =

    response = {
        'token': token,
    }

    return JsonResponse(response)
