from django.urls import path
from leads import views

urlpatterns = [
    # Leads endpoints
    path("leads", views.LeadView.as_view()),
]
