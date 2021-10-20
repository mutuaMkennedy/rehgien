from . import serializers
from location import models
from rest_framework.generics import ListAPIView
import django_filters


class DistrictsListApi(ListAPIView):
    queryset = models.Districts.objects.all()
    serializer_class = serializers.DistrictsSerializer

class DivisionsListApi(ListAPIView):
    queryset = models.Divisions.objects.all()
    serializer_class = serializers.DivisionsSerializer

class KNPolytechnicsListApi(ListAPIView):
    queryset = models.KenyaNationalPolytechnics.objects.all()
    serializer_class = serializers.KNPolytechnicsSerializer

class KenyaPrimarySchoolsListApi(ListAPIView):
    queryset = models.KenyaPrimarySchools.objects.all()
    serializer_class = serializers.KenyaPrimarySchoolsSerializer

class PrivateCollegesListApi(ListAPIView):
    queryset = models.PrivateColleges.objects.all()
    serializer_class = serializers.PrivateCollegesSerializer

class PrivateUniversitiesListApi(ListAPIView):
    queryset = models.PrivateUniversities.objects.all()
    serializer_class = serializers.PrivateUniversitiesSerializer

class PublicCollegesListApi(ListAPIView):
    queryset = models.PublicColleges.objects.all()
    serializer_class = serializers.PublicCollegesSerializer

class UniversitiesCollegesListApi(ListAPIView):
    queryset = models.UniversitiesColleges.objects.all()
    serializer_class = serializers.UniversitiesCollegesSerializer

class SecondarySchoolsListApi(ListAPIView):
    queryset = models.SecondarySchools.objects.all()
    serializer_class = serializers.SecondarySchoolsSerializer

class TeachersTrainingCollegesListApi(ListAPIView):
    queryset = models.TeachersTrainingColleges.objects.all()
    serializer_class = serializers.TTCollegesSerializer

class UniversitiesListApi(ListAPIView):
    queryset = models.Universities.objects.all()
    serializer_class = serializers.UniversitiesSerializer

class KenyaTownsFilter(django_filters.FilterSet):
    town_name = django_filters.rest_framework.CharFilter(field_name="town_name", lookup_expr='icontains')
    class Meta:
        model = models.KenyaTown
        fields = {
            'town_name'
        }

class KenyaTownListApi(ListAPIView):
    queryset = models.KenyaTown.objects.all()
    serializer_class = serializers.KenyaTownSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = KenyaTownsFilter
