from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
		path('account/', views.profile, name='account'),
		path('agents/<int:pk>/detail', views.agent_detail, name = 'agent_detail'),
		path('accounts/profile/edit', views.edit_profile, name='edit_profile'),
		path('agents/', views.agent_list, name = 'agent_list'),
]
