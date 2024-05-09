from django.db import models
from choices import Choices
from applicants.models import Applicants
from utils import generate_cafID
from user_auth.models import Comments, BaseModel
from customer.models import CustomerDetails


# class CafDetails(BaseModel):

#     caf_id = models.CharField(max_length=255, default=generate_cafID, unique=True)
#     pdWith = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
#     # customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
#     applicant = models.OneToOneField(Applicants, on_delete=models.CASCADE, related_name='applicant_id', null=True)
#     tentative_amt = models.FloatField(max_length=15, null=True, blank=True)
#     placeOfPdAddress = models.TextField(null=True,blank=True)
#     location = models.CharField(max_length=255, null=True, blank=True)
#     extra_data = models.JSONField(null=True, blank=True)
#     description = models.TextField(null=True)
#     comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

class CustomerApplicationForm(BaseModel):

    caf_id = models.CharField(max_length=255, default=generate_cafID, unique=True)
    pdWith = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
    # customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
    applicant = models.OneToOneField(Applicants, on_delete=models.CASCADE, related_name='applicant_id', null=True)
    tentative_amt = models.FloatField(max_length=15, null=True, blank=True)
    placeOfPdAddress = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)