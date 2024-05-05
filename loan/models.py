from django.db import models
from applicants.models import Applicants
from utils import generate_locanID
from user_auth.models import Comments
from choices import Choices

class Loan(models.Model):
    
    loan_id = models.CharField(max_length=255, default=generate_locanID, unique=True)
    applicant = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name='Applicant')
    product_type = models.CharField(max_length=255, choices=Choices.PRODUCT_TYPE_CHOICES, null=True)
    transaction_type = models.CharField(max_length=255, choices=Choices.TRANSACTION_TYPE, null= True, default='automatic')
    case_tag = models.CharField(max_length=255, null=True, choices=Choices.CASE_TAG_CHOICES)
    applied_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    applied_tenure = models.IntegerField()
    applied_ROI = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

    processing_fees = models.JSONField(null=True)

    valuation_charges = models.JSONField(null=True)

    legal_and_incidental_fee = models.JSONField(null=True)

    stamp_duty_applicable_rate = models.JSONField(null=True)

    rcu_charges_applicable_rate = models.JSONField(null=True)

    stamping_expenses_applicable_rate = models.JSONField(null=True)
