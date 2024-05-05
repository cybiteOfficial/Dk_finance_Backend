from django.urls import path
from .views import Customer_CafAPIView,UploadDocumentAPIView,PhotographUploadAPIView


urlpatterns = [
    path('caf_detail', Customer_CafAPIView.as_view(), name='Customer_CafAPIView'),


    path('documents/', UploadDocumentAPIView.as_view(), name='document-list'),
    path('documents/<int:pk>/', UploadDocumentAPIView.as_view(), name='document-detail'),

     path('photographs/', PhotographUploadAPIView.as_view(), name='photograph-list'),
    path('photographs/<int:pk>/', PhotographUploadAPIView.as_view(), name='photograph-detail'),
]
