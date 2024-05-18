from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.models import BaseModel,User, Comments
from leads.models import Leads
from choices import Choices
from applicants.models import Applicants

 

class KYCDetails(BaseModel):
    lead_id = models.ForeignKey(Leads, on_delete=models.DO_NOTHING, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_number = PhoneNumberField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)
    kyc_verified = models.BooleanField(null=True, blank=True)
    kyc_document_verified = models.BooleanField(null=True, blank=True)


class DocumentsUpload(BaseModel):
    document_name = models.CharField(max_length=255, null=True, blank=True)
    document_id = models.CharField(max_length=255, null=True, blank=True)
    file = models.CharField(max_length=300)
    document_type = models.CharField(max_length=255, choices=Choices.DOCUMENT_TYPE_CHOICES)
    kyc = models.ForeignKey(KYCDetails, on_delete=models.DO_NOTHING, null=True, related_name="kyc_details", blank=True)
    application = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name="application", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True, blank=True)