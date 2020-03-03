from location.api.serializers import (
            DistrictsSerializer,
            DivisionsSerializer,
            KNPolytechnicsSerializer,
            KenyaPrimarySchoolsSerializer,
            PrivateCollegesSerializer,
            PrivateUniversitiesSerializer,
            PublicCollegesSerializer,
            UniversitiesCollegesSerializer,
            SecondarySchoolsSerializer,
            TTCollegesSerializer,
            UniversitiesSerializer
            )
from location.models import (
            Districts,
            Divisions,
            KenyaNationalPolytechnics,
            KenyaPrimarySchools,
            PrivateColleges,
            PrivateUniversities,
            PublicColleges,
            UniversitiesColleges,
            SecondarySchools,
            TeachersTrainingColleges,
            Universities
            )
from rest_framework.generics import ListAPIView



class DistrictsListApi(ListAPIView):
    queryset = Districts.objects.all()
    serializer_class = DistrictsSerializer

class DivisionsListApi(ListAPIView):
    queryset = Divisions.objects.all()
    serializer_class = DivisionsSerializer

class KNPolytechnicsListApi(ListAPIView):
    queryset = KenyaNationalPolytechnics.objects.all()
    serializer_class = KNPolytechnicsSerializer

class KenyaPrimarySchoolsListApi(ListAPIView):
    queryset = KenyaPrimarySchools.objects.all()
    serializer_class = KenyaPrimarySchoolsSerializer

class PrivateCollegesListApi(ListAPIView):
    queryset = PrivateColleges.objects.all()
    serializer_class = PrivateCollegesSerializer

class PrivateUniversitiesListApi(ListAPIView):
    queryset = PrivateUniversities.objects.all()
    serializer_class = PrivateUniversitiesSerializer

class PublicCollegesListApi(ListAPIView):
    queryset = PublicColleges.objects.all()
    serializer_class = PublicCollegesSerializer

class UniversitiesCollegesListApi(ListAPIView):
    queryset = UniversitiesColleges.objects.all()
    serializer_class = UniversitiesCollegesSerializer

class SecondarySchoolsListApi(ListAPIView):
    queryset = SecondarySchools.objects.all()
    serializer_class = SecondarySchoolsSerializer

class TeachersTrainingCollegesListApi(ListAPIView):
    queryset = TeachersTrainingColleges.objects.all()
    serializer_class = TTCollegesSerializer

class UniversitiesListApi(ListAPIView):
    queryset = Universities.objects.all()
    serializer_class = UniversitiesSerializer
