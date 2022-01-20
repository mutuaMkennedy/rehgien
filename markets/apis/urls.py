from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('markets/job_post/list/', views.JobPostListApi.as_view(), name='JobPostListApi'),
    path('markets/job_post/create/', views.JobPostCreateApi.as_view(), name='JobPostCreateApi'),
    path('markets/job_post/<int:pk>/', views.JobPostDetailApi.as_view(), name='JobPostDetailApi'),
    path('markets/job_post/<int:pk>/update/', views.JobPostUpdateApi.as_view(), name='JobPostUpdateApi'),
    path('markets/job_post/<int:pk>/add_viewer/', views.JobPostViewerUpdateApi.as_view(), name='JobPostViewerUpdateApi'),
    path('markets/job_post_proposal/create/', views.JobPostProposalCreateApi.as_view(), name='JobPostProposalCreateApi'),
    # Project
    path('markets/project/list/', views.ProjectListApi.as_view(), name='ProjectListApi'),
    path('markets/project/create/', views.ProjectCreateApi.as_view(), name='ProjectCreateApi'),
    path('markets/project/<int:pk>/retrieve/', views.ProjectDetailApi.as_view(), name='ProjectDetailApi'),
    path('markets/project/<int:pk>/update/', views.ProjectUpdateApi.as_view(), name='ProjectUpdateApi'),

]
