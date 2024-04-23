from django.db import models
from user_auth.models import BaseModel
from user_auth.models import User
# from customer.models import CustomerDetails
from leads.models import Leads
from phonepay.models import Payment
from utils import generate_applicationID
from choices import Choices


class Applicants(BaseModel):
    
    application_id = models.CharField(max_length=255, default=generate_applicationID)
    lead = models.OneToOneField(Leads, on_delete=models.CASCADE, related_name='leads')
    paymentedetails = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='paymentdetail')
    status = models.CharField(max_length=200, choices= Choices.APPLICATION_STATUS_CHOICES, default='in_progress')

    def __str__(self) -> str:
        return self.application_id