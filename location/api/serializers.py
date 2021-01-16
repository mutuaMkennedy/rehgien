from rest_framework import serializers
from location import models

class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Districts
        fields= '__all__'

class DivisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Divisions
        fields= '__all__'

class KNPolytechnicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KenyaNationalPolytechnics
        fields= '__all__'

class KenyaPrimarySchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KenyaPrimarySchools
        fields= '__all__'

class PrivateCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivateColleges
        fields= '__all__'

class PrivateUniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivateUniversities
        fields= '__all__'

class PublicCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PublicColleges
        fields= '__all__'

class UniversitiesCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UniversitiesColleges
        fields= '__all__'

class SecondarySchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecondarySchools
        fields= '__all__'

class TTCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeachersTrainingColleges
        fields= '__all__'

class UniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Universities
        fields= '__all__'

class KenyaTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KenyaTown
        fields= '__all__'
