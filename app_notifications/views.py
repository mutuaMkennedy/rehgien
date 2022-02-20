from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import JsonResponse

User = get_user_model()

def mark_notifications_read(request):
    user = User.objects.get(pk=request.user.pk)
    user.notifications.mark_all_as_read()
    notifications = user.notifications.all
    context = {
        "notifications":notifications
    }
    html = render_to_string('app_notifications/notifications_section.html', context, request=request)
    return JsonResponse({'page_section':html})