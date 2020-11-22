from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'location'

urlpatterns = [
	path('districts_dataset/', views.districts_dataset, name='districts_data'),
	path('divisions_dataset/', views.divisions_dataset, name='divisions_data'),
	path('polytechnics_dataset/', views.polytechnics_dataset, name='polytechnics_data'),
	path('private_colleges_dataset/', views.private_colleges_dataset, name='private_colleges_data'),
	path('private_universities_dataset/', views.private_universities_dataset, name='private_universities_data'),
	path('public_colleges_dataset/', views.public_colleges_dataset, name='public_colleges_data'),
	path('university_colleges_dataset/', views.university_colleges_dataset, name='university_colleges_data'),
	path('secondary_schools_dataset/', views.secondary_schools_dataset, name='secondary_schools_data'),
	path('universities_dataset/', views.universities_dataset, name='universities_data'),
	path('primary_schools_dataset/', views.primary_schools_dataset, name='primary_schools_data'),
	path('teachers_training_dataset/', views.teachers_training_dataset, name='teachers_training_data'),
]
