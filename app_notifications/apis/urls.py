from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('notifications/list/', views.NotificationsListApi.as_view(), name='NotificationsListApi'),
    path('notifications/<int:pk>/update/', views.NotificationsUpdateApi.as_view(), name='NotificationsUpdateApi'),
    path('notifications/device/list/', views.DeviceInformationListApi.as_view(), name='DeviceInformationListApi'),
    path('notifications/device/create/', views.DeviceInformationCreateApi.as_view(), name='DeviceInformationCreateApi'),
    path('notifications/device/<int:pk>/update/', views.DeviceInformationUpdateApi.as_view(), name='DeviceInformationUpdateApi'),
]
