from django.urls import path, re_path
from . import views
from . import profile_edit_views as peViews

app_name = 'profiles'

urlpatterns = [
		path('account/', views.account_page, name='account'),
		path('account/user/change_to_pro/', views.change_user_type_to_pro, name='change_to_pro'),
		path('home/', views.business_homepage, name='business_homepage'),
		path('accounts/nu_profile/edit', views.edit_basic_profile, name='edit_basic_profile'),
		path('search/service', views.ajax_autocomplete, name='pro_service_ajx_search'),
		path('categories/', views.business_list, name = 'business_list'),
		path('view_more/<int:pk>/', views.business_detail, name = 'business_detail'),
		path('write/review/', views.business_review, name = 'business_review'),
		path('review/like/', views.like_review, name = 'like_review'),
		path('accounts/business_profile/<int:pk>/editor_mode', peViews.business_page_editor_mode, name='pro_business_page_edit'),
		path('accounts/business_profile/update/<int:pk>/<slug:slug>', peViews.busines_profile_update, name='business_profile_update'),

		path('portfolio_item/add/', views.portfolio_item_create, name = 'portfolio_item_create'),
		path('portfolio_item/<int:pk>/update/', views.portfolio_item_update, name='portfolio_item_update'),

		# save and follow routes
		path('pro/save/', views.pro_save, name='save_pro'),
		path('pro/follow/', views.pro_follow, name='follow_pro'),
		# add to team
		path('pro/connect/request/', views.request_connection, name='request_connection'),
		path('pro/connetion/remove/', views.remove_connection, name='remove_connection'),
		path('my_network/connections/', views.user_connections, name='user_connections'),
		path('pro/following/', views.user_followers, name='user_followers'),
		path('notifications/', views.notifications, name='notifications'),
]
