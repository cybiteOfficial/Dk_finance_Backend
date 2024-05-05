from django.db import models
from choices import Choices
from applicants.models import Applicants
from utils import generate_CollateralID
from user_auth.models import Comments, BaseModel

class CollateralDetails(BaseModel):
    collateral_id = models.CharField(max_length=255, default=generate_CollateralID, unique=True)
    applicant = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name='Applicant_collateral')
    collateralType = models.CharField(max_length=255, null=True)
    collateralName = models.CharField(max_length=255)
    primarySecondary = models.CharField(max_length=255, null=True)
    valuationRequired = models.CharField(max_length=255, null=True)
    relationshipWithLoan = models.CharField(max_length=255, null=True)
    propertyOwner = models.CharField(max_length=255, null=True)
    propertyCategory = models.CharField(max_length=255, null=True)
    propertyType = models.CharField(max_length=255, null=True)
    occupationStatus = models.CharField(max_length=255, null=True)
    propertyStatus = models.CharField(max_length=255, null=True)
    propertyTitle = models.CharField(max_length=255, null=True)
    houseFlatShopNo = models.CharField(max_length=255, null=True)
    khasraPlotNo = models.CharField(max_length=255, null=True)
    locality = models.CharField(max_length=255, null=True)
    village = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    taluka = models.CharField(max_length=255, null=True)
    pincode = models.CharField(max_length=10, null=True)
    landmark = models.CharField(max_length=255, null=True)
    estimatedPropertyValue = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    documentName = models.CharField(max_length=255, null=True)
    documentUpload = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)
    isExisting = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.collateralName
