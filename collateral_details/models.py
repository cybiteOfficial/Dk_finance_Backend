from django.db import models
from choices import Choices
from applicants.models import Applicants
from utils import generate_CollateralID
from user_auth.models import Comments

class CollateralDetails(models.Model):
    collateral_id = models.CharField(max_length=255, default=generate_CollateralID, unique=True)
    applicant = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name='Applicant_collateral')
    collateralType = models.CharField(max_length=255, null=True, blank=True)
    collateralName = models.CharField(max_length=255, blank=True)
    primarySecondary = models.CharField(max_length=255, null=True, blank=True)
    valuationRequired = models.CharField(max_length=255, null=True, blank=True)
    relationshipWithLoan = models.CharField(max_length=255, null=True, blank=True)
    propertyOwner = models.CharField(max_length=255, null=True, blank=True)
    propertyCategory = models.CharField(max_length=255, null=True, blank=True)
    propertyType = models.CharField(max_length=255, null=True, blank=True)
    occupationStatus = models.CharField(max_length=255, null=True, blank=True)
    propertyStatus = models.CharField(max_length=255, null=True, blank=True)
    propertyTitle = models.CharField(max_length=255, null=True, blank=True)
    houseFlatShopNo = models.CharField(max_length=255, null=True, blank=True)
    khasraPlotNo = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    taluka = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    estimatedPropertyValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    documentName = models.CharField(max_length=255, null=True, blank=True)
    documentUpload = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True, blank=True)
    isExisting = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.collateralName
