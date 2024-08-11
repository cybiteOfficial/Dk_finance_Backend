from django.urls import path
from .views import CustomerDetailsAPIView, KYCVerifyView

urlpatterns = [
    path('customers', CustomerDetailsAPIView.as_view(), name='customer-details'),
    path('verify_kyc', KYCVerifyView.as_view())
]
