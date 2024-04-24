from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.models import BaseModel, Comments
from leads.models import Leads
from choices import Choices
from applicants.models import Applicants

class KYCDetails(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_number = PhoneNumberField()
    email = models.EmailField(max_length=100)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

class DocumentsUpload(BaseModel):
    document_name = models.CharField(max_length=255, null=True)
    document_id = models.CharField(max_length=255, null=True)
    file = models.CharField(max_length=300)
    document_type = models.CharField(max_length=255, choices=Choices.DOCUMENT_TYPE_CHOICES)
    kyc = models.ForeignKey(KYCDetails, on_delete=models.DO_NOTHING, null=True, related_name="kyc_details")
    application = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name="application", null=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)