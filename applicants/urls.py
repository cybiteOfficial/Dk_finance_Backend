from django.urls import path
from .views import ApplicantAPIView

urlpatterns = [
    path('applicants/', ApplicantAPIView.as_view(), name='applicant'),
]
