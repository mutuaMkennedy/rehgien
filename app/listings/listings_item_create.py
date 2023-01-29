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


#script for creating dummy data
#Note: disable compressImage function in models file before run
def createHomes():
    innitial_home = get_object_or_404(models.Home,pk=1)
    user = User.objects.get(pk=1)

    home_json = json.loads(serialize('json', models.Home.objects.all()))
    jsonItem = home_json[0]['fields']
    jsonItem.pop('publishdate', None)
    jsonItem.pop('saves', None)
    #for sale homes
    for home in range(0,50):
        type_array = [
            'APARTMENT', 'BUNGALOW', 'CONDOMINIUM',
            'DORMITORY', 'DUPLEX', 'MANSION', 'SINGLEFAMILY',
            'TERRACED', 'TOWNHOUSE',
            'OTHER'
        ]
        price = randrange(1000000,100000000)
        bathrooms = randrange(1,6)
        bedrooms = randrange(1,6)
        floor_area = randrange(900,1250)
        lat = randrange(250,290)
        long =  randrange(750,790)
        type = ''

        type_choice = randrange(0,9)
        type = type_array[type_choice]

        jsonItem['listing_type'] = 'for_sale'
        jsonItem['price'] = price
        jsonItem['bathrooms'] = bathrooms
        jsonItem['bedrooms'] = bedrooms
        jsonItem['floor_area'] = floor_area
        jsonItem['owner'] = user
        jsonItem['type'] = type
        jsonItem['location'] = 'SRID=4326;POINT (36.' + str(long) + ' -1.' + str(lat) +')'
        home = models.Home.objects.create(**jsonItem)
        home.save()
        photos = [
            'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8MXx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8OXx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTl8fGhvdXNlfGVufDB8fDB8&auto=format&fit=crop&w=500&q=60'
            ]
        for img in photos:
            file_instance = models.PropertyPhoto(
                    photo = img,\
                    home = models.Home.objects.get(id=home.id))
            file_instance.save()

    #rental homes
    for home in range(0,50):
        type_array = [
            'APARTMENT', 'BUNGALOW', 'CONDOMINIUM',
            'DORMITORY', 'DUPLEX', 'MANSION', 'SINGLEFAMILY',
            'TERRACED', 'TOWNHOUSE',
            'OTHER'
        ]
        price = randrange(1000,10000000)
        bathrooms = randrange(1,6)
        bedrooms = randrange(1,6)
        floor_area = randrange(900,1250)
        lat = randrange(230,290)
        long =  randrange(750,890)
        type = ''

        type_choice = randrange(0,9)
        type = type_array[type_choice]

        jsonItem['listing_type'] = 'for_rent'
        jsonItem['price'] = price
        jsonItem['bathrooms'] = bathrooms
        jsonItem['bedrooms'] = bedrooms
        jsonItem['floor_area'] = floor_area
        jsonItem['owner'] = user
        jsonItem['type'] = type
        jsonItem['location'] = 'SRID=4326;POINT (36.' + str(long) + ' -1.' + str(lat) +')'
        home = models.Home.objects.create(**jsonItem)
        home.save()
        photos = [
            'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8MXx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8OXx8aG91c2V8ZW58MHx8MHw%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTl8fGhvdXNlfGVufDB8fDB8&auto=format&fit=crop&w=500&q=60'
            ]
        for img in photos:
            file_instance = models.PropertyPhoto(
                    photo = img,\
                    home = models.Home.objects.get(id=home.id))
            file_instance.save()
