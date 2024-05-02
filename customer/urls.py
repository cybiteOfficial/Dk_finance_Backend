from django.urls import path
from .views import CustomerDetailsAPIView

urlpatterns = [
    path('customers', CustomerDetailsAPIView.as_view(), name='customer-details'),
]
