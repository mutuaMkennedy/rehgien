from django.urls import path, re_path
from . import views

app_name = 'app_accounts'

urlpatterns = [
    path('auth/login/', views.user_login, name='user_login'),
]
