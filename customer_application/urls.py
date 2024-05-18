from django.urls import path
from .views import CafFomAPIView


urlpatterns = [
    path('caf_detail', CafFomAPIView.as_view(), name='Customer_CafAPIView'),
]


