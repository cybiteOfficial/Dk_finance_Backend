from django.urls import path
from .views import ApplicantAPIView, CreateAppForPaymentReference

urlpatterns = [
    path('applicants/', ApplicantAPIView.as_view(), name='applicant'),
    path('create_app_id', CreateAppForPaymentReference.as_view()),
]
