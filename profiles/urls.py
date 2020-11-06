from django.urls import path
from . import views
from . import profile_edit_views as peViews

app_name = 'profiles'

urlpatterns = [
		path('account/', views.profile, name='account'),
		path('accounts/nu_profile/edit', views.edit_basic_profile, name='edit_basic_profile'),

		path('business/', views.business_list, name = 'business_list'),
		path('business/<int:pk>/', views.business_detail, name = 'business_detail'),
		path('business/write/review/', views.business_review, name = 'business_review'),
		path('accounts/company_profile/<int:pk>/editor_mode', peViews.company_profile_editor_mode, name='co_profile_edit_mode'),
		path('accounts/company_profile/update/<int:pk>/<slug:slug>', peViews.company_profile_update, name='company_profile_update'),

		path('agents/', views.agent_list, name = 'agent_list'),
		path('agents/<int:pk>/', views.agent_detail, name = 'agent_detail'),
		path('agent/write/review/', views.agent_review, name = 'agent_review'),
		path('accounts/ag_profile/<int:pk>/editor_mode', peViews.agent_profile_editor_mode, name='ag_profile_edit_mode'),
		path('accounts/ag_profile/update/<int:pk>/<slug:slug>', peViews.agent_profile_update, name='agent_profile_update'),


		path('propertyManagers/', views.property_manager_list, name = 'pm_list'),
		path('propertyManagers/<int:pk>/', views.property_manager_detail, name = 'pm_detail'),
		path('propertyManager/write/review/', views.property_manager_review, name = 'pm_review'),
		path('accounts/propertyManager_profile/<int:pk>/editor_mode', peViews.pm_profile_editor_mode, name='pm_profile_edit_mode'),
		path('accounts/propertyManager_profile/update/<int:pk>/<slug:slug>', peViews.pm_profile_update, name='pm_profile_update'),

		path('design&service/', views.dservice_pros_list, name = 'd_service_list'),
		path('design&service/<int:pk>/', views.dservice_pros_detail, name = 'd_service_detail'),
		path('design&service/write/review/', views.dservice_pros_review, name = 'd_service_review'),
		path('accounts/design&service/<int:pk>/editor_mode', peViews.ds_profile_editor_mode, name='ds_profile_edit_mode'),
		path('accounts/design&service/update/<int:pk>/<slug:slug>', peViews.ds_profile_update, name='ds_profile_update'),

		# pro portfolio & project crud routes
		path('portfolio_item/add', views.pm_portfolio_create, name = 'pm_portfolio_create'),
		path('portfolio_item/<int:pk>/update/', views.pm_portfolio_update, name='pm_portfolio_update'),
		path('project/add', views.DS_project_create, name = 'DS_project_create'),
		path('project/<int:pk>/update/', views.DS_project_update, name='DS_project_update'),

		# save and follow routes
		path('pro/save_company/', views.save_company, name='save_company'),
		path('pro/follow_company/', views.follow_company, name='follow_company'),
		path('pro/save_agent/', views.save_agent, name='save_agent'),
		path('pro/follow_agent/', views.follow_agent, name='follow_agent'),
		path('pro/save_pm/', views.save_pm, name='save_pm'),
		path('pro/follow_pm/', views.follow_pm, name='follow_pm'),
		path('pro/save_ds/', views.save_ds, name='save_ds'),
		path('pro/follow_ds/', views.follow_ds, name='follow_ds'),
		path('pro/pro_follow/', views.pro_follow, name='pro_follow'),
		# add to team
		path('pro/connect/request/', views.request_connection, name='request_connection'),
		path('pro/connetion/remove/', views.remove_connection, name='remove_connection'),
		path('my_network/connections/', views.user_connections, name='user_connections'),
		path('pro/following/', views.user_followers, name='user_followers'),
]
