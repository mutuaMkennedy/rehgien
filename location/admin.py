from django.contrib import admin
from .models import (Districts, Divisions, KenyaNationalPolytechnics,
					KenyaPrimarySchools, PrivateColleges, PrivateUniversities,
					PublicColleges, UniversitiesColleges,
					SecondarySchools, TeachersTrainingColleges, Universities,KenyaTown
					)
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class DistrictsAdmin(LeafletGeoAdmin):
	list_display = ('name_0', 'name_1', 'name_2', 'geom')

class DivisionsAdmin(LeafletGeoAdmin):
	list_display = ('name_0', 'name_1', 'name_2', 'name_3', 'geom')

class KenyaNationalPolytechnicsAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class KenyaPrimarySchoolsAdmin(LeafletGeoAdmin):
	list_display = ('name_of_sc', 'status', 'geom')

class PrivateCollegesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class PrivateUniversitiesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class PublicCollegesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class UniversitiesCollegesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class SecondarySchoolsAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class TeachersTrainingCollegesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class UniversitiesAdmin(LeafletGeoAdmin):
	list_display = ('name', 'descriptio', 'geom')

class KenyaTownsAdmin(LeafletGeoAdmin):
	list_display = ('town_name', 'town_type','geom')

admin.site.register(Districts, LeafletGeoAdmin)
admin.site.register(Divisions, LeafletGeoAdmin)
admin.site.register(KenyaNationalPolytechnics, LeafletGeoAdmin)
admin.site.register(KenyaPrimarySchools, LeafletGeoAdmin)
admin.site.register(PrivateColleges, LeafletGeoAdmin)
admin.site.register(PrivateUniversities, LeafletGeoAdmin)
admin.site.register(PublicColleges, LeafletGeoAdmin)
admin.site.register(UniversitiesColleges, LeafletGeoAdmin)
admin.site.register(SecondarySchools, LeafletGeoAdmin)
admin.site.register(TeachersTrainingColleges, LeafletGeoAdmin)
admin.site.register(Universities, LeafletGeoAdmin)
admin.site.register(KenyaTown, KenyaTownsAdmin)
