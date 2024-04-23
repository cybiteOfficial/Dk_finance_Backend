from django.db import models
from user_auth.models import BaseModel, User
from leads.models import Leads
from choices import Choices
from utils import generate_PaymentID

# Create your models here.
class Payment(BaseModel):

    payment_id = models.CharField(max_length=255, unique=True, default=generate_PaymentID)
    lead_id = models.OneToOneField(Leads, on_delete=models.DO_NOTHING, related_name='lead')
    order_id = models.CharField(max_length=255, unique=True)  # Unique identifier for your order
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in decimal format
    currency = models.CharField(max_length=3)  # Optional: Currency code (e.g., INR)
    status = models.CharField(max_length=255, choices=Choices.PAYMENT_STATUS, blank=False, null=False)  # Track payment status (e.g., initiated, pending, successful, failed)

    def __str__(self) -> str:
        return self.payment_id