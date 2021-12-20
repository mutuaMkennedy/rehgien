from django.urls import path, re_path
from . import views
from . import profile_edit_views as peViews

app_name = 'profiles'

urlpatterns = [
		# path('categories/pros/home/', views.business_homepage, name='business_homepage'),
		# path('search/service', views.ajax_autocomplete, name='pro_service_ajx_search'),
		# path('categories/', views.business_list, name = 'business_list'),
		# path('view_more/<int:pk>/', views.business_detail, name = 'business_detail'),
		# path('write/review/', views.business_review, name = 'business_review'),
		# path('review/like/', views.like_review, name = 'like_review'),
		path('accounts/business_profile/<int:pk>/', peViews.business_page_editor_mode, name='pro_business_page_edit'),
		path('accounts/business_profile/update/<int:pk>/<slug:slug>', peViews.busines_profile_update, name='business_profile_update'),
		# path('accounts/wish_list/', views.user_wishlist, name='user_wishlist'),
		# path('accounts/wish_list/saved_properties/', views.user_saved_properties, name='user_saved_properties'),
		# path('accounts/wish_list/saved_pros/', views.saved_pros, name='saved_pros'),
		# path('accounts/wish_list/saved_searches/', views.saved_searches, name='saved_searches'),
		# path('accounts/projects/', views.projects, name='projects'),
		# path('accounts/my_reviews/', views.reviews, name='pro_reviews_list'),
		# path('accounts/settings/', views.account_settings, name='account_settings'),
		# path('accounts/settings/edit_account/', views.edit_account_info, name='edit_account_info'),
		# path('accounts/my_jobs/', views.my_jobs, name='my_jobs'),
		# path('accounts/home/', views.user_is_signed_in_homepage, name='user_is_signed_in_homepage'),
		#
		path('portfolio_item/add/', views.portfolio_item_create, name = 'portfolio_item_create'),
		path('portfolio_item/<int:pk>/update/', views.portfolio_item_update, name='portfolio_item_update'),
		#
		# # save and follow routes
		# path('pro/save/', views.pro_save, name='save_pro'),
		# path('pro/follow/', views.pro_follow, name='follow_pro'),
		# # add to team
		# path('pro/connect/request/', views.request_connection, name='request_connection'),
		# path('pro/connection/remove/', views.remove_connection, name='remove_connection'),
		# path('pro/connection/request/action/', views.connection_request_action, name='connection_request_action'),
		# path('my_network/connections/', views.user_connections, name='user_connections'),
		# path('pro/following/', views.user_followers, name='user_followers'),
		# path('notifications/', views.notifications, name='notifications'),

]
