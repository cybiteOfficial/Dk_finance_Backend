from django.urls import path
from leads import views

urlpatterns = [
    # Leads endpoints
    path("leads", views.LeadView.as_view()),
    path("leads_web", views.LeadViewForWeb.as_view()) # for admin site.

]
