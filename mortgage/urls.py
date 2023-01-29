from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'mortgage'
urlpatterns = [
	url(r'^lending_institutions/$', views.mortgagehomepage, name='mortgagehomepage'),
	url(r'^cooperative/$', views.mortgage_calculator, name='coop_calculator'),
]