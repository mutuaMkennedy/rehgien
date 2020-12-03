from . import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json
from random import randrange
User = get_user_model()


#create n number of users
def createUsers():
    for user in range(0,50):
        new_user = User.objects.create(
            username = "abcPro"+ str(user),
            user_type = 'PRO',
            password = "zoom20$$",
            email = "mutuakennedy81@gmail.com"
            )
        new_user.save()

def createProfiles():
    for user in range(0,50):
        new_user = User.objects.create(
            username = "abcPro"+ str(user),
            user_type = 'PRO',
            password = "zoom20$$",
            email = "mutuakennedy81@gmail.com"
            )
        new_user.save()
