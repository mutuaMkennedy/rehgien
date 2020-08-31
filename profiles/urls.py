from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
		path('account/', views.profile, name='account'),
		path('agents/', views.agent_list, name = 'agent_list'),
		path('agents/<int:pk>/', views.agent_detail, name = 'agent_detail'),
		path('accounts/nu_profile/edit', views.edit_n_user_profile, name='edit_n_user_profile'),# Normal User profile form
		path('accounts/ag_profile/edit', views.edit_agent_profile, name='edit_ag_profile'),# agent profile form
		path('accounts/pm_profile/edit', views.edit_pm_profile, name='edit_pm_profile'),# property Manager profile form
		path('accounts/ds_profile/edit', views.edit_ds_profile, name='edit_ds_profile'),# Design service pros profile form
		path('agent/write/review/', views.agent_review, name = 'agent_review'),
		path('propertyManagers/', views.property_manager_list, name = 'pm_list'),
		path('propertyManagers/<int:pk>/', views.property_manager_detail, name = 'pm_detail'),
		path('propertyManager/write/review/', views.property_manager_review, name = 'pm_review'),
		path('design&service/', views.dservice_pros_list, name = 'd_service_list'),
		path('design&service/<int:pk>/', views.dservice_pros_detail, name = 'd_service_detail'),
		path('design&service/write/review/', views.dservice_pros_review, name = 'd_service_review'),
]
