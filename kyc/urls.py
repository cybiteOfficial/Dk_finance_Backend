from django.urls import path
from kyc import views

urlpatterns = [
    # Kyc endpoints
    path("kyc", views.KYCVIew.as_view()),
]   
