from django import template
from django.template.defaultfilters import stringfilter
from django.shortcuts import get_object_or_404
from profiles import models as profiles_models

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def split_str(value):
    return value.split(',')

@register.simple_tag
def question_answers(service, user):
    results = []
    for question in service.matchmaking_service.matchmaker_question.all():
        # print(question.title)
        for answer in question.pro_question_answer.filter(business_profile = user.pro_business_profile.pk ):
            # print(answer)
            for selected_option in answer.answer.all():
                # print(option)
                results.append(selected_option.pk)
    return results

@register.simple_tag
def question_service_areas(service, user):
    results = []
    question = service.matchmaking_service.matchmaker_question.all().first()
    answer = question.pro_question_answer.filter(business_profile = user.pro_business_profile.pk )
    if answer.exists():
        for service_area in answer.first().service_delivery_areas.all():
            data = {
                'id':service_area.pk,
                'town_name':service_area.town_name
            }
            results.append(data)
    return results

@register.simple_tag
def active_services(user):
    results = []
    profile = get_object_or_404(profiles_models.BusinessProfile, pk=user.pro_business_profile.pk )
    for selected_service in profile.professional_services.all():
        results.append(selected_service.pk)
    return results
