from rest_framework import serializers
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

class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Districts
        fields=[
        'name_2', 'geom'
        ]

class DivisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Divisions
        fields=[
        'name_3', 'geom'
        ]

class KNPolytechnicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KenyaNationalPolytechnics
        fields=[
        'name','descriptio','geom'
        ]

class KenyaPrimarySchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KenyaPrimarySchools
        fields=[
        'name_of_sc','geom'
        ]

class PrivateCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateColleges
        fields=[
        'name','geom'
        ]

class PrivateUniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateUniversities
        fields=[
        'name','geom'
        ]

class PublicCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicColleges
        fields=[
        'name','geom'
        ]

class UniversitiesCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversitiesColleges
        fields=[
        'name','geom'
        ]

class SecondarySchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondarySchools
        fields=[
        'institute','geom'
        ]

class TTCollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model =TeachersTrainingColleges
        fields=[
        'name','geom'
        ]

class UniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model =Universities
        fields=[
        'name','geom'
        ]
