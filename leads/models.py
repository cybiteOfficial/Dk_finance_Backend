from django.db import models
from utils import generate_leadID
from choices import Choices
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.models import BaseModel, User

class Leads(BaseModel):

    lead_id = models.CharField(max_length=255, default=generate_leadID, unique=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='leads')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    mobile_number = PhoneNumberField()
    agent_code = models.CharField(max_length=255, null=True)
    branch_code = models.CharField(max_length=255, null=True)
    branch_name = models.CharField(max_length=255, null=True)
    loan_amount = models.CharField(max_length=255, null=True)
    product_type = models.CharField(max_length=255, choices=Choices.PRODUCT_TYPE_CHOICES, default='normal')
    case_tag = models.CharField(max_length=255, choices=Choices.CASE_TAG_CHOICES, default='normal')
    customer_type = models.CharField(max_length=255, choices=Choices.CUSTOMER_TYPE_CHOICES, default='home_loan')
    source = models.CharField(max_length=255, choices=Choices.LEAD_SOURCE_TYPE, default='website')

    def __str__(self) -> str:
        return self.lead_id

