from django.db import models
from user_auth.models import BaseModel
from applicants.models import Applicants


# Create your models here.
class CustomerDetails(BaseModel):
    
    cif_id = models.CharField(max_length=255)
    applicant = models.OneToOneField(Applicants, on_delete=models.DO_NOTHING, related_name='applicant')
    customer_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    case_tag = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=255)
    agent_code = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255)
    load_amount = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    dob = models.DateTimeField()
    age = models.IntegerField()
    gender = models.CharField(max_length=255)
    customer_segment = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    source_of_income = models.CharField(max_length=255)
    monthly_income = models.IntegerField()
    monthly_family_income = models.IntegerField()
    questions = models.BooleanField()
    current_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    kyc_id = models.CharField(max_length=255)
    # profile_photo = models.CharField(max_length=255)
    profile_photo = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    # familydetails = models.ForeignKey('FamilyDetails', on_delete=models.CASCADE, related_name='familydetails')
    # education = models.ForeignKey('Education', on_delete=models.CASCADE, related_name='education')
    # collateral = models.ForeignKey('CollateralDetails', on_delete=models.CASCADE, related_name='collateraldetails')

    def __str__(self) -> str:
        return self.cif_id