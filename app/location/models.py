from django.db import models
from django.contrib.gis.db import models


# Create your models here.

class Districts(models.Model):
    id_0 = models.BigIntegerField() # Country code
    iso = models.CharField(max_length=3) # KEN
    name_0 = models.CharField(max_length=75) # Country name
    id_1 = models.BigIntegerField() # province ID
    name_1 = models.CharField(max_length=75) # Province name
    id_2 = models.BigIntegerField() # District ID
    name_2 = models.CharField(max_length=75) #District name
    type_2 = models.CharField(max_length=50)
    engtype_2 = models.CharField(max_length=50) # district
    nl_name_2 = models.CharField(max_length=75)
    varname_2 = models.CharField(max_length=150)
    geom = models.MultiPolygonField(srid=4326)


    class Meta:
    	verbose_name_plural = 'Districts'

    def __str__(self):
    	return self.name_0 + '-' + self.name_1 + '-' + self.name_2


class Divisions(models.Model):
    id_0 = models.BigIntegerField() # Country code
    iso = models.CharField(max_length=3) # KEN
    name_0 = models.CharField(max_length=75) # Country name
    id_1 = models.BigIntegerField() # province ID
    name_1 = models.CharField(max_length=75) # Province name
    id_2 = models.BigIntegerField() # District ID
    name_2 = models.CharField(max_length=75) # District name
    id_3 = models.BigIntegerField() # Division Id
    name_3 = models.CharField(max_length=75) # Division name
    type_3 = models.CharField(max_length=50)
    engtype_3 = models.CharField(max_length=50)
    nl_name_3 = models.CharField(max_length=75)
    varname_3 = models.CharField(max_length=100)
    geom = models.MultiPolygonField(srid=4326)


    class Meta:
    	verbose_name_plural = 'Divisions'

    def __str__(self):
    	return self.name_0 + '-' + self.name_1 + '-' + self.name_2 + '-' + self.name_3


# Nationwide Datasets go here

class KenyaNationalPolytechnics(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'KenyaNationalPolytechnics'

    def __str__(self):
        return self.name + '-' + self.descriptio

class KenyaPrimarySchools(models.Model):
    fid = models.BigIntegerField()
    name_of_sc = models.CharField(max_length=80)
    level_field = models.CharField(max_length=80)
    status = models.CharField(max_length=80)
    type1 = models.CharField(max_length=80)
    type2 = models.CharField(max_length=80)
    type3 = models.CharField(max_length=80)
    latitude = models.FloatField()
    longitude = models.FloatField()
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'KenyaPrimarySchools'

    def __str__(self):
        return self.name_of_sc

class PrivateColleges(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'PrivateColleges'

    def __str__(self):
        return self.name + '-' + self.descriptio

class PrivateUniversities(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'PrivateUniversities'

    def __str__(self):
        return self.name + '-' + self.descriptio

class PublicColleges(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'PublicColleges'

    def __str__(self):
        return self.name + '-' + self.descriptio

class UniversitiesColleges(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'UniversitiesColleges'

    def __str__(self):
        return self.name + '-' + self.descriptio

class SecondarySchools(models.Model):
    institute = models.CharField(max_length=40)
    latitude = models.FloatField()
    longitude = models.FloatField()
    district = models.CharField(max_length=20)
    division = models.CharField(max_length=30)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'SecondarySchools'

    def __str__(self):
        return self.institute

class TeachersTrainingColleges(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'TeachersTrainingColleges'

    def __str__(self):
        return self.name + '-' + self.descriptio

class Universities(models.Model):
    name = models.CharField(max_length=80)
    descriptio = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name + '-' + self.descriptio

class KenyaTown(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    town_name = models.CharField(max_length=254)
    town_id = models.FloatField()
    town_type = models.CharField(max_length=254)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        verbose_name_plural = 'KenyaTowns'

    def __str__(self):
        return self.town_name 
