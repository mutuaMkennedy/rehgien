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
	path('districts/', DistrictsListApi.as_view(), name='districts_list'),
    path('divisions/', DivisionsListApi.as_view(), name='division_list'),
    path('kenya-national-polytechnics/', KNPolytechnicsListApi.as_view(), name='KNPolytechnics_list'),
    path('kenya-primary-schools/', KenyaPrimarySchoolsListApi.as_view(), name='primary_schools_list'),
    path('private-colleges/', PrivateCollegesListApi.as_view(), name='private_colleges_list'),
    path('private-universities/', PrivateUniversitiesListApi.as_view(), name='private_universities_list'),
    path('public-colleges/', PublicCollegesListApi.as_view(), name='public_colleges_list'),
    path('university-colleges/', UniversitiesCollegesListApi.as_view(), name='university_colleges_list'),
    path('secondary-schools/', SecondarySchoolsListApi.as_view(), name='secondary_schools_list'),
    path('teachers-colleges/', TeachersTrainingCollegesListApi.as_view(), name='teachers_colleges_list'),
    path('universities/', UniversitiesListApi.as_view(), name='universities_list'),

]
