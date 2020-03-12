from django.urls import path
from django.conf.urls import url
from .views import (
        DistrictsListApi,
        DivisionsListApi,
        KNPolytechnicsListApi,
        KenyaPrimarySchoolsListApi,
        PrivateCollegesListApi,
        PrivateUniversitiesListApi,
        PublicCollegesListApi,
        UniversitiesCollegesListApi,
        SecondarySchoolsListApi,
        TeachersTrainingCollegesListApi,
        UniversitiesListApi
        )



urlpatterns = [
	path('location/districts/', DistrictsListApi.as_view(), name='districts_list'),
    path('location/divisions/', DivisionsListApi.as_view(), name='division_list'),
    path('location/kenya-national-polytechnics/', KNPolytechnicsListApi.as_view(), name='KNPolytechnics_list'),
    path('location/kenya-primary-schools/', KenyaPrimarySchoolsListApi.as_view(), name='primary_schools_list'),
    path('location/private-colleges/', PrivateCollegesListApi.as_view(), name='private_colleges_list'),
    path('location/private-universities/', PrivateUniversitiesListApi.as_view(), name='private_universities_list'),
    path('location/public-colleges/', PublicCollegesListApi.as_view(), name='public_colleges_list'),
    path('location/university-colleges/', UniversitiesCollegesListApi.as_view(), name='university_colleges_list'),
    path('location/secondary-schools/', SecondarySchoolsListApi.as_view(), name='secondary_schools_list'),
    path('location/teachers-colleges/', TeachersTrainingCollegesListApi.as_view(), name='teachers_colleges_list'),
    path('location/universities/', UniversitiesListApi.as_view(), name='universities_list'),

]
