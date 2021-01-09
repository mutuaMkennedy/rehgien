from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('markets/job_post/list/', views.JobPostListApi.as_view(), name='JobPostListApi'),
    path('markets/job_post/create/', views.JobPostCreateApi.as_view(), name='JobPostCreateApi'),
    path('markets/job_post/<int:pk>/', views.JobPostDetailApi.as_view(), name='JobPostDetailApi'),
    path('markets/job_post/<int:pk>/update/', views.JobPostUpdateApi.as_view(), name='JobPostUpdateApi'),
    path('markets/job_post/<int:pk>/add_viewer/', views.JobPostViewerUpdateApi.as_view(), name='JobPostViewerUpdateApi'),
]
