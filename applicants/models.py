from django.db import models
from user_auth.models import BaseModel
from user_auth.models import User
# from customer.models import CustomerDetails
from leads.models import Leads
from phonepay.models import Payment
from utils import generate_applicationID

# Create your models here.
class Applicants(BaseModel):
    
    application_id = models.CharField(max_length=255, default=generate_applicationID)
    lead = models.OneToOneField(Leads, on_delete=models.CASCADE, related_name='leads')
    paymentedetails = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='paymentdetail')
    # customer = models.ForeignKey(CustomerDetails, on_delete=models.DO_NOTHING, related_name='customerdetails')

    def __str__(self) -> str:
        return self.application_id