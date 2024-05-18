from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanAPIView

urlpatterns = [
    path('loan_details', LoanAPIView.as_view()),
]
