from django.urls import path
from .views import Customer_CafAPIView


urlpatterns = [
    path('Customer_CafAPIView', Customer_CafAPIView.as_view(), name='Customer_CafAPIView'),
]


