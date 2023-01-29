from django import template
from markets import models as markets_model
from django.utils.timesince import timesince

register = template.Library()

@register.simple_tag
def project_lead(pk):
    project = markets_model.Project.objects.filter(pk=int(pk))
    array=""
    if project.exists():
        array = {
            "pk":project[0].pk,
            "service":project[0].requested_service.service_name,
            "service_avatar":project[0].requested_service.service_image.url,
            "message": project[0].client_message[:50],
            "publishdate":timesince(project[0].publishdate)
        }
    return array
