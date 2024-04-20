from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.models import BaseModel
from leads.models import Leads
from choices import Choices

class KYCDetails(BaseModel):
    lead = models.ForeignKey(Leads, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_number = PhoneNumberField()
    email = models.EmailField(max_length=100)

class DocumentsUpload(BaseModel):
    document_name = models.CharField(max_length=255)
    document_id = models.CharField(max_length=255, null=True)
    file = models.CharField(max_length=300)
    document_type = models.CharField(max_length=255, choices=Choices.DOCUMENT_TYPE_CHOICES)
    kyc = models.ForeignKey(KYCDetails, on_delete=models.DO_NOTHING, null=True)
