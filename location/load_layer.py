import os
from django.contrib.gis.utils import LayerMapping
from .models import (Districts, Divisions,
                    KenyaNationalPolytechnics, KenyaPrimarySchools, PrivateColleges,
                    PrivateUniversities, PublicColleges, UniversitiesColleges,
                    SecondarySchools, TeachersTrainingColleges, Universities,KenyaTown
                    )


districts_mapping = {
    'id_0': 'ID_0',
    'iso': 'ISO',
    'name_0': 'NAME_0',
    'id_1': 'ID_1',
    'name_1': 'NAME_1',
    'id_2': 'ID_2',
    'name_2': 'NAME_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'nl_name_2': 'NL_NAME_2',
    'varname_2': 'VARNAME_2',
    'geom': 'MULTIPOLYGON',
}


Districts_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_adm2.shp'))

def run(verbose=True):
	lm = LayerMapping(Districts, Districts_shp, districts_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)


divisions_mapping = {
    'id_0': 'ID_0',
    'iso': 'ISO',
    'name_0': 'NAME_0',
    'id_1': 'ID_1',
    'name_1': 'NAME_1',
    'id_2': 'ID_2',
    'name_2': 'NAME_2',
    'id_3': 'ID_3',
    'name_3': 'NAME_3',
    'type_3': 'TYPE_3',
    'engtype_3': 'ENGTYPE_3',
    'nl_name_3': 'NL_NAME_3',
    'varname_3': 'VARNAME_3',
    'geom': 'MULTIPOLYGON',
}

Divisions_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_adm3.shp'))

def run2(verbose=True):
	lm = LayerMapping(Divisions, Divisions_shp, divisions_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

# Nationwide datasets imported to database here
#dictionary for national polytechnics
kenyanationalpolytechnics_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_national_polytechnic_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_National_Polytechnics/National_Polytechnics-point.shp'))

def polytechnics_run(verbose=True):
	lm = LayerMapping(KenyaNationalPolytechnics, Ken_national_polytechnic_shp, kenyanationalpolytechnics_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for kenya primary schools
kenyaprimaryschools_mapping = {
    'fid': 'FID',
    'name_of_sc': 'Name_of_Sc',
    'level_field': 'Level_',
    'status': 'Status',
    'type1': 'Type1',
    'type2': 'Type2',
    'type3': 'Type3',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'geom': 'MULTIPOINT',
}

Ken_primary_schools_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Primary_Schools/Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp'))

def primary_schools_run(verbose=True):
	lm = LayerMapping(KenyaPrimarySchools, Ken_primary_schools_shp, kenyaprimaryschools_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for Private colleges
privatecolleges_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_private_colleges_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Private_Colleges/Private_Colleges-point.shp'))

def private_colleges_run(verbose=True):
	lm = LayerMapping(PrivateColleges, Ken_private_colleges_shp, privatecolleges_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for private universities
privateuniversities_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_private_universities_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Private_Universities/Private_Universities-point.shp'))

def private_universities_run(verbose=True):
	lm = LayerMapping(PrivateUniversities, Ken_private_universities_shp, privateuniversities_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for public colleges
publiccolleges_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_public_colleges_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Public_Colleges/Public_Colleges-point.shp'))

def public_colleges_run(verbose=True):
	lm = LayerMapping(PublicColleges, Ken_public_colleges_shp, publiccolleges_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for public university colleges
universitiescolleges_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_university_colleges_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Public_Universities/Public_University_Constituent_Colleges-point.shp'))

def university_colleges_run(verbose=True):
	lm = LayerMapping(UniversitiesColleges, Ken_university_colleges_shp, universitiescolleges_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for secondary schools
secondaryschools_mapping = {
    'institute': 'INSTITUTE',
    'latitude': 'LATITUDE',
    'longitude': 'LONGITUDE',
    'district': 'DISTRICT',
    'division': 'DIVISION',
    'geom': 'MULTIPOINT',
}

Ken_secondary_schools_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Secondary_Schools/KEN_SecondarySchools.shp'))

def secondary_schools_run(verbose=True):
	lm = LayerMapping(SecondarySchools, Ken_secondary_schools_shp, secondaryschools_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for teachers training colleges
teacherstrainingcolleges_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_teachers_training_colleges_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Teacher_Training_Colleges/Teacher_Trainer_Colleges-point.shp'))

def teachers_training_run(verbose=True):
	lm = LayerMapping(TeachersTrainingColleges, Ken_teachers_training_colleges_shp, teacherstrainingcolleges_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

#dictionary for universities
universities_mapping = {
    'name': 'Name',
    'descriptio': 'descriptio',
    'geom': 'MULTIPOINT',
}

Ken_universities_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/KEN_Universities/UNIVERSITIES-point.shp'))

def universities_run(verbose=True):
	lm = LayerMapping(Universities, Ken_universities_shp, universities_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)

# Kenya all towns
kenyatowns_mapping = {
    'area': 'AREA',
    'perimeter': 'PERIMETER',
    'town_name': 'TOWN_NAME',
    'town_id': 'TOWN_ID',
    'town_type': 'TOWN_TYPE',
    'geom': 'MULTIPOINT',
}

kenya_all_towns_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'GisData/kenya_all_towns/kenya_all_towns.shp'))

def add_towns(verbose=True):
	lm = LayerMapping(KenyaTown, kenya_all_towns_shp, kenyatowns_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)
