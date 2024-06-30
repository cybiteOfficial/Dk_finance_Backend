from django.db import models
from utils import generate_leadID, generate_agent_code
from choices import Choices
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.models import BaseModel, User, Comments

class Leads(BaseModel):

    lead_id = models.CharField(max_length=255, default=generate_leadID, unique=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='leads', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True)
    mobile_number = PhoneNumberField()
    agent_code = models.CharField(max_length=255, null=True, default=generate_agent_code)
    branch_code = models.CharField(max_length=255, null=True)
    branch_name = models.CharField(max_length=255, null=True)
    loan_amount = models.CharField(max_length=255, null=True)
    product_type = models.CharField(max_length=255, choices=Choices.PRODUCT_TYPE_CHOICES, default='normal')
    case_tag = models.CharField(max_length=255, choices=Choices.CASE_TAG_CHOICES, default='normal')
    customer_type = models.CharField(max_length=255, choices=Choices.CUSTOMER_TYPE_CHOICES, default='home_loan')
    source = models.CharField(max_length=255, choices=Choices.SOURCE_TYPE, default='website')
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

    def __str__(self) -> str:
        return self.lead_id

