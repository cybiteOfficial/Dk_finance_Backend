from django.db import models
from user_auth.models import BaseModel
from user_auth.models import User
# from customer.models import CustomerDetails
from leads.models import Leads
from phonepay.models import Payment
from utils import generate_applicationID
from choices import Choices
from user_auth.models import Comments


class Applicants(BaseModel):
    
    application_id = models.CharField(max_length=255, default=generate_applicationID)
    lead = models.OneToOneField(Leads, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    paymentedetails = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='paymentdetail')
    status = models.CharField(max_length=200, choices= Choices.APPLICATION_STATUS_CHOICES, default='ro_phase')
    description = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.application_id

class AuditTrail(BaseModel):
    current_status = models.CharField(max_length=255, null=True, blank=True)
    updated_status =models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    application_id = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING)