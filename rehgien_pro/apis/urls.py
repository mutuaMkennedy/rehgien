from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # Leads
    path('pro/leads/list/', views.LeadsListApi, name='LeadsListApi'),

]
