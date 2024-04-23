from django.db import models
from user_auth.models import BaseModel
from applicants.models import Applicants
from utils import generate_customerID



# Create your models here.
class CustomerDetails(BaseModel):
    
    cif_id = models.CharField(max_length=255, default=generate_customerID, unique=True)
    applicant = models.OneToOneField(Applicants, on_delete=models.DO_NOTHING, related_name='applicant')
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    # product_type = models.CharField(max_length=255)
    # case_tag = models.CharField(max_length=255)
    # customer_type = models.CharField(max_length=255, default='Unknow', null=True)
    # agent_code = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # branch_code = models.CharField(max_length=255)
    load_amount = models.CharField(max_length=255, null=True)
    source = models.CharField(max_length=255, default='website', null=True)
    title = models.CharField(max_length=255)
    dateOfBirth = models.CharField()
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    customerSegment = models.CharField(max_length=255, null=True)
    # industry = models.CharField(max_length=255, null=True)
    # occupation = models.CharField(max_length=255, default='Worker', null=True)
    sourceOfIncome = models.CharField(max_length=255, default='Business', null=True)
    monthlyIncome = models.CharField(default=10000)
    monthlyFamilyIncome = models.CharField(default=10000)
    residenceOwnership = models.CharField(max_length=255, null=True)
    agriculturalLand = models.CharField(max_length=255, null=True)
    valueOfAgriculturalLand = models.CharField(null=True)
    earningsFromAgriculturalLand = models.CharField(null=True)
    educationQualification = models.CharField(255, null=True)
    numberOfDependents = models.CharField(null=True)

    # questions = models.BooleanField(default=False, null=True)
    current_address = models.CharField(max_length=255, null=True)
    permanent_address = models.CharField(max_length=255,null=True)
    # kyc_id = models.(max_length=255)
    # profile_photo = models.CharField(max_length=255)
    profile_photo = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    # familydetails = models.ForeignKey('FamilyDetails', on_delete=models.CASCADE, related_name='familydetails')
    # education = models.ForeignKey('Education', on_delete=models.CASCADE, related_name='education')
    # collateral = models.ForeignKey('CollateralDetails', on_delete=models.CASCADE, related_name='collateraldetails')

    def __str__(self) -> str:
        return self.cif_id