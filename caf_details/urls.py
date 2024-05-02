from django.urls import path
from .views import Customer_CafAPIView


urlpatterns = [
    path('caf_detail', Customer_CafAPIView.as_view(), name='Customer_CafAPIView'),
]


