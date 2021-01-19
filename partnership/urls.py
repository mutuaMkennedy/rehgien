from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'partnership'

urlpatterns = [
    path('partner/', views.partner_program_home, name = 'partner_program_home'),
    path('partner/application/', views.partnership_form, name = 'partnership_form'),
]
