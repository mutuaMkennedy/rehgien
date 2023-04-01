from django.urls import path, re_path
from . import views

app_name = 'app_notifications'

urlpatterns = [
    path('mark_as_read/', views.mark_notifications_read, name='mark_notifications_read'),
]
