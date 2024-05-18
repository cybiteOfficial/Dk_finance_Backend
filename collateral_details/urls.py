from django.urls import path
from .views import CollateralDetailsAPIView

urlpatterns = [
    path('collateral_details', CollateralDetailsAPIView.as_view(), name='collateral-details'),
]
