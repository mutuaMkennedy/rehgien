from django.urls import path
from django.conf.urls import url
from . import views



urlpatterns = [
	path('location/districts/list/', views.DistrictsListApi.as_view(), name='districts_list'),
    path('location/divisions/list/', views.DivisionsListApi.as_view(), name='division_list'),
    path('location/kenya_national_polytechnics/list/', views.KNPolytechnicsListApi.as_view(), name='KNPolytechnics_list'),
    path('location/kenya_primary_schools/list/', views.KenyaPrimarySchoolsListApi.as_view(), name='primary_schools_list'),
    path('location/private_colleges/list/', views.PrivateCollegesListApi.as_view(), name='private_colleges_list'),
    path('location/private_universities/list/', views.PrivateUniversitiesListApi.as_view(), name='private_universities_list'),
    path('location/public_colleges/list/', views.PublicCollegesListApi.as_view(), name='public_colleges_list'),
    path('location/university_colleges/list/', views.UniversitiesCollegesListApi.as_view(), name='university_colleges_list'),
    path('location/secondary_schools/list/', views.SecondarySchoolsListApi.as_view(), name='secondary_schools_list'),
    path('location/teachers_colleges/list/', views.TeachersTrainingCollegesListApi.as_view(), name='teachers_colleges_list'),
    path('location/universities/', views.UniversitiesListApi.as_view(), name='universities_list'),
    path('location/kenya_towns/list/', views.KenyaTownListApi.as_view(), name='KenyaTownListApi'),

]
