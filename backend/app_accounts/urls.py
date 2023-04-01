from django.urls import path, re_path
from . import views

app_name = 'app_accounts'

urlpatterns = [
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/signup/', views.user_signup, name='user_signup'),
    path('auth/signup/setup/', views.UserAccountSetupWizardView.as_view(views.FORMS), name='UserAccountSetupWizard'),
    path('validate_phone/',views.validate_phone_send_otp, name='validate_phone')
]
