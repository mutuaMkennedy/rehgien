from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
		path('account/', views.profile, name='account'),
		path('agents/', views.agent_list, name = 'agent_list'),
		path('agents/<int:pk>/', views.agent_detail, name = 'agent_detail'),
		path('accounts/profile/edit', views.edit_profile, name='edit_profile'),
		path('agent/write/review/', views.agent_review, name = 'agent_review'),
		path('propertyManagers/', views.property_manager_list, name = 'pm_list'),
		path('propertyManagers/<int:pk>/', views.property_manager_detail, name = 'pm_detail'),
		path('propertyManager/write/review/', views.property_manager_review, name = 'pm_review'),
		path('design&service/', views.dservice_pros_list, name = 'd_service_list'),
		path('design&service/<int:pk>/', views.dservice_pros_detail, name = 'd_service_detail'),
		path('design&service/write/review/', views.dservice_pros_review, name = 'd_service_review'),
]
