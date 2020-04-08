from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
		path('account/', views.profile, name='account'),
		path('account/<int:pk>/edit/', views.edit_profile, name='edit_profile')
]
