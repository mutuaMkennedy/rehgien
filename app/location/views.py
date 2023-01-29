from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import authentication, permissions
from . import  models
from .serializer import SalePropertySerializer
from rest_framework.generics import ListAPIView
from .pagination import ListingGeoJsonPagination
from rest_framework.renderers import JSONRenderer
try:
	from django.utils import simplejson as simplejson
except ImportError:
	import json


def map_box(request):
	mapbox_access_token = 'pk.eyJ1IjoicmV5a2VubmVkeSIsImEiOiJjam9td3ZkMnYwdjB5M3ZueWQ1YzVocThwIn0.PBVWnwga3qG6KX6_CoPy8g'
	return render(request, 'location/mapbox.html', {'mapbox_access_token':mapbox_access_token})


def divisions_dataset(request):
	data1 = serialize('geojson', models.Divisions.objects.all())
	return HttpResponse(data1, content_type='json')

def districts_dataset(request):
	data2 = serialize('geojson', models.Districts.objects.all())
	return HttpResponse(data2, content_type='json')

def polytechnics_dataset(request):
	kpoly = serialize('geojson', models.KenyaNationalPolytechnics.objects.all())
	return HttpResponse(kpoly, content_type='json')

def primary_schools_dataset(request):
	primary_schools = serialize('geojson', models.KenyaPrimarySchools.objects.all())
	return HttpResponse(primary_schools, content_type='json')

def private_colleges_dataset(request):
	private_colleges = serialize('geojson', models.PrivateColleges.objects.all())
	return HttpResponse(private_colleges, content_type='json')

def private_universities_dataset(request):
	private_universities = serialize('geojson', models.PrivateUniversities.objects.all())
	return HttpResponse(private_universities, content_type='json')

def public_colleges_dataset(request):
	public_colleges = serialize('geojson', models.PublicColleges.objects.all())
	return HttpResponse(public_colleges, content_type='json')

def university_colleges_dataset(request):
	university_colleges = serialize('geojson', models.UniversitiesColleges.objects.all())
	return HttpResponse(university_colleges, content_type='json')

def secondary_schools_dataset(request):
	secondary_schools = serialize('geojson', models.SecondarySchools.objects.all())
	return HttpResponse(secondary_schools, content_type='json')

def teachers_training_dataset(request):
	teachers_training = serialize('geojson', models.TeachersTrainingColleges.objects.all())
	return HttpResponse(teachers_training, content_type='json')

def universities_dataset(request):
	universities = serialize('geojson', models.Universities.objects.all())
	return HttpResponse(universities, content_type='json')

def get_towns(request):
	q = str(request.GET.get('term', ''))
	towns = models.KenyaTown.objects.filter(town_name__icontains = q)
	results = []
	for town in towns:
		print(town)
		results.append(town.town_name.capitalize())
	data = json.dumps(results)

	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
