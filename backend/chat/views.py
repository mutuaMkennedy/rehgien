from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from profiles.models import BusinessProfile
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.core.serializers import serialize
from . twilio import conversations
import json

# referencing the custom user model
User = get_user_model()

# Twilio chat
def get_twilio_acess_token(request):
    if request.user.is_authenticated:
        identity = request.user.pk
        token = conversations.get_token(identity)
        return JsonResponse({'token':token})

    else:
        return JsonResponse({'Unauthorized':'You are not autheticated.'})

def deleteConversation(request):
    if request.user.is_authenticated:
        convoSID = request.GET.get('sid','')
        if convoSID:
            response = conversations.deleteConversation(convoSID)
            return JsonResponse({'status':response})
        else:
            return JsonResponse({'status':False,'detail':'Conversation sid is required!'})
    return JsonResponse({'status':False,'detail':'Permission Denied'})
