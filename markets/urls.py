from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'markets'

urlpatterns = [
    # path('job_post/', views.job_post_home, name = 'job_post_home'),
    # path('job_post/create/', views.job_post_create, name = 'job_post_create'),
    # path('job_post/<int:pk>/update/', views.job_post_update, name = 'job_post_update'),
    # path('job_post/<int:pk>/deactivate/', views.job_post_deactivate, name = 'job_post_deactivate'),
    # path('job_post/search_pros/', views.ajax_search_pros, name = 'ajax_search_pros'),
    # path('job_post/search_service/', views.ajax_search_service, name = 'ajax_search_service'),
    # path('job_post/<int:pk>/', views.job_post_detail, name = 'job_post_detail'),
    # path('find_customers/jobs/submit_proposal/<int:pk>/', views.submit_proposal, name = 'submit_proposal'),
    path('project/ajax/', views.ajax_get_project, name = 'ajax_get_project'),    

]
