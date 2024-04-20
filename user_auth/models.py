import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from validators import validate_otp_length
from choices import Choices

class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PersonDetails(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Choices.GENDER_CHOICES, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)


class BankDetails(BaseModel):
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20, unique=True)
    branch_code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    currency = models.CharField(max_length=10, default="INR")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    

class User(BaseModel, AbstractUser, PersonDetails):
    
    username =  models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=250, choices=Choices.USER_TYPE_CHOICES)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    otp = models.IntegerField(validators=[validate_otp_length], null=True, blank=True)
    bank_branch = models.ForeignKey(BankDetails, on_delete=models.DO_NOTHING)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = "User"
        permissions = [
            ("can_view", "Can view"),
            ("can_change", "Can change"),
            ("can_delete", "Can delete"),
        ]   