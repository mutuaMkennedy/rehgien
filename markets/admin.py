from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import (
                    PropertyRequestLead,
                    ProffesionalRequestLead,
                    OtherServiceLead,
                    AgentLeadRequest,
                    AgentPropertyRequest
                    )


class AgentLeadRequestAdmin(LeafletGeoAdmin):
	list_display = ('property_type','ownership','qualified')

class AgentPropertyRequestAdmin(LeafletGeoAdmin):
	list_display = ('property_type','ownership','qualified')

admin.site.register(PropertyRequestLead)
admin.site.register(ProffesionalRequestLead)
admin.site.register(OtherServiceLead)
admin.site.register(AgentLeadRequest, AgentLeadRequestAdmin)
admin.site.register(AgentPropertyRequest, AgentPropertyRequestAdmin)
