# phonepay/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('initiate-payment/', views.PhonePePaymentView.as_view(), name='initiate_payment'),
]
