from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # Leads
    path('payments/mpesa/stkpush/pay/', views.pay_with_mpesa, name='pay_with_mpesa'),
    # Leads
    path('payments/mpesa/b2c/settle_payment/', views.settle_mpesa_payment, name='lipa_na_mpesa'),

]
