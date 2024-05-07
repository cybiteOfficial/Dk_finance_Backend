from django.db import models
from user_auth.models import BaseModel
from applicants.models import Applicants
from utils import generate_customerID
from choices import Choices
from user_auth.models import Comments

class CustomerDetails(BaseModel):
    
    cif_id = models.CharField(max_length=255, default=generate_customerID, unique=True)
    applicant = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name='applicant')

    # common for android and admin
    title = models.CharField(max_length=50, choices=Choices.TITLE_CHOICES, null=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=30, null=True)
    dateOfBirth = models.CharField()
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=Choices.GENDER_CHOICES)
    
    loan_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    source = models.CharField(max_length=255, choices=Choices.SOURCE_TYPE, default='website', null=True)

    # for android
    customerSegment = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    occupation = models.CharField(max_length=255, default='Worker', null=True)
    sourceOfIncome = models.CharField(max_length=255, default='Business', null=True)
    monthlyIncome = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    monthlyFamilyIncome = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    residenceOwnership = models.CharField(max_length=255, null=True)
    agriculturalLand = models.CharField(max_length=255, null=True)
    valueOfAgriculturalLand = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    earningsFromAgriculturalLand = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    educationQualification = models.CharField(255, null=True)
    numberOfDependents = models.IntegerField(null=True, default=1)

    current_address = models.CharField(max_length=255, null=True)
    permanent_address = models.CharField(max_length=255,null=True)
    profile_photo = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

    def __str__(self) -> str:
        return self.cif_id

class CustomerAddress(BaseModel):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.DO_NOTHING)
    is_current = models.BooleanField(default=True)
    is_permanent = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    address_line_3 = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    tehsil_or_taluka = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    residence_state = models.CharField(max_length=255, null=True, blank=True)
    residence_type = models.CharField(max_length=255, null=True, blank=True)
    stability_at_residence = models.CharField(max_length=255, null=True, blank=True)
    distance_from_branch = models.CharField(max_length=255, null=True, blank=True)