import random
import string
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from user_auth.validators import validate_otp_length


def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)


# class PersonDetails(models.Model):
#     class Meta:
#         abstract = True
    
#     GENDER_CHOICES = [
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('other', 'Other'),
#     ]
    
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
#     phone_number = PhoneNumberField(blank=True, null=True)


# class BankDetails(BaseModel):
#     bank_name = models.CharField(max_length=100)
#     branch_name = models.CharField(max_length=100)
#     ifsc_code = models.CharField(max_length=20, unique=True)
#     branch_code = models.CharField(max_length=20, unique=True)
#     address = models.TextField(blank=True, null=True)
#     country = models.CharField(max_length=100, default="India")
#     state = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     pincode = models.CharField(max_length=20)
#     currency = models.CharField(max_length=10, default="INR")


# class User(BaseModel, AbstractUser, PersonDetails):
#     USER_TYPE_CHOICES = [
#         ("ro", "Ro"), 
#         ("do", "Do"), 
#         ("technicalofficer", "Technicalofficer"), 
#         ("bm", "Bm"),
#         ("md", "MD"),
#         ("cluster", "Cluster")
#     ]
#     username =  models.CharField(max_length=250)
#     email = models.EmailField(max_length=100, unique=True)
#     user_type = models.CharField(max_length=250, choices=USER_TYPE_CHOICES)
#     profile_picture = models.ImageField(
#         upload_to="profile_pictures/", blank=True, null=True
#     )
#     otp = models.IntegerField(validators=[validate_otp_length], null=True, blank=True)
#     bank_branch = models.ForeignKey(BankDetails, on_delete=models.DO_NOTHING)
#     aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['username']

#     def __str__(self) -> str:
#         return self.username

#     def save(self, *args, **kwargs):
#         UserModel = get_user_model()
#         if not self.username:
#             self.username = self.email.split("@")[0]

#             try:
#                 UserModel.objects.get(username=self.username)
#                 self.username = generate_random_string()
#             except Exception:
#                 pass

#         super().save(*args, **kwargs)

#     class Meta:
#         db_table = "User"


from django.db import models

class Leads(BaseModel):
    
    lead_id = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    email_id = models.EmailField()
    product_type = models.CharField(max_length=255)
    case_tag = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=255)
    agent_code = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255)
    load_amount = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    # assigned_to = models.CharField(max_length=255)
    assigned_to = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='leads')

    def __str__(self) -> str:
        return self.lead_id


class BankDetails(BaseModel):
    
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)  

    def __str__(self) -> str:
        return self.branch_code

class PaymentDetails(BaseModel):
    
    status = models.BooleanField()
    amount = models.IntegerField()
    method = models.CharField(max_length=255)
    application_id = models.OneToOneField('Applicants', on_delete=models.DO_NOTHING, related_name='application')
    

class IdentificationDetails(BaseModel):
    
    # application_id = models.CharField(max_length=255)
    application_id = models.OneToOneField('Applicants', on_delete=models.DO_NOTHING, related_name='application')
    kyc_batch_id = models.CharField(max_length=255)
    proof_type = models.CharField(max_length=255)
    document_type = models.CharField(max_length=255)
    document_id = models.CharField(max_length=255)
    kyc_status = models.BooleanField()
    kyc_verified = models.BooleanField()
    verification_type = models.CharField(max_length=255)


class Applicants(BaseModel):
    
    application_id = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    email_id = models.EmailField()
    # assigned_to = models.CharField(max_length=255)
    assigned_to = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user')
    paymentedetails = models.OneToOneField('PaymentDetails', on_delete=models.CASCADE, related_name='paymentdetail')
    identification = models.ForeignKey(IdentificationDetails, on_delete=models.CASCADE, related_name='IdentificationDetails')
    loan = models.OneToOneField('LoanDetails', on_delete=models.DO_NOTHING, related_name='loan')
    customer = models.ForeignKey('CustomerDetails', on_delete=models.DO_NOTHING, related_name='customerdetails')
    
    otp_verification = models.IntegerField()

    def __str__(self) -> str:
        return self.application_id


class User(BaseModel, AbstractUser):
    
    user_id = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    password = models.IntegerField()
    # branch_code = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)
    # role = models.CharField(max_length=255)

    bankdetails = models.ForeignKey(BankDetails, on_delete=models.DO_NOTHING, related_name='users')
    leads = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='leads')
    applicants = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applicant')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user_id

class CustomerDetails(BaseModel):
    
    cif_id = models.CharField(max_length=255)
    applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applicant')
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

    familydetails = models.ForeignKey('FamilyDetails', on_delete=models.CASCADE, related_name='familydetails')
    education = models.ForeignKey('Education', on_delete=models.CASCADE, related_name='education')
    collateral = models.ForeignKey('CollateralDetails', on_delete=models.CASCADE, related_name='collateraldetails')

    def __str__(self) -> str:
        return self.cif_id
    

class ApplicationFlow(BaseModel):
    
    application_id = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING, related_name='applicant')
    ro_id = models.IntegerField()
    dm_id = models.IntegerField()
    TO_id = models.IntegerField()
    BM_id = models.IntegerField()
    Cluster_id = models.IntegerField()
    ro_status = models.CharField(max_length=255)
    dm_status = models.CharField(max_length=255)
    TO_status = models.CharField(max_length=255)
    BM_Status = models.CharField(max_length=255)
    rejected_by = models.CharField(max_length=255)
    cluster_status = models.CharField(max_length=255)


class FamilyDetails(BaseModel):
    
    customer_id = models.OneToOneField(CustomerDetails, on_delete=models.DO_NOTHING, related_name='customer')
    no_of_family = models.IntegerField()
    no_of_children = models.IntegerField()
    age_of_elder_child = models.IntegerField()
    no_of_dependent = models.IntegerField()
    no_of_earning_modes = models.IntegerField()
    relation = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    document_id = models.CharField(max_length=255)
    document_proof = models.CharField(max_length=255) 

    # customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, related_name='family_details')   
    

class Education(BaseModel):
    
    customer_id = models.OneToOneField(CustomerDetails, on_delete=models.DO_NOTHING, related_name='customer')
    qualification = models.CharField(max_length=255)
    agri_land = models.CharField(max_length=255)
    tentative_value = models.IntegerField()
    residence_station = models.CharField(max_length=255)
    value_of_residentat = models.CharField(max_length=255)
    legal_notes = models.CharField(max_length=255)
    

class LoanDetails(BaseModel):
    
    loan_id = models.CharField(max_length=255)
    application_id = models.OneToOneField(Applicants, on_delete=models.DO_NOTHING, related_name='applicant')
    product_type = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    case_tag = models.CharField(max_length=255)
    applied_loan_amount = models.CharField(max_length=255)
    applied_tenure = models.CharField(max_length=255)
    applied_ROI = models.CharField(max_length=255)
    

class CollateralDetails(BaseModel):
    
    customer_id = models.OneToOneField(CustomerDetails, on_delete=models.DO_NOTHING, related_name='customer')
    is_existing_collateral = models.BooleanField(default=True)
    collateral_type = models.CharField(max_length=255)
    collateral_name = models.CharField(max_length=255)
    Primary_secondary = models.CharField(max_length=255)
    Valuation = models.CharField(max_length=255)
