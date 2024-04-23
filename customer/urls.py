from django.urls import path
from .views import CustomerDetailsAPIView

urlpatterns = [
    path('customer-details/', CustomerDetailsAPIView.as_view(), name='customer-details'),
]
