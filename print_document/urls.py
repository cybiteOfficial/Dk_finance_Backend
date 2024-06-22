from django.urls import path
from print_document import views

urlpatterns = [
    path("print_document", views.PrintDocumentView.as_view()),
]
