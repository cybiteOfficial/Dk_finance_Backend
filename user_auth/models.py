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
    updated_at = models.DateTimeField(auto_now=True)


class PersonDetails(models.Model):
    class Meta:
        abstract = True
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
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


class User(BaseModel, AbstractUser, PersonDetails):
    USER_TYPE_CHOICES = [
        ("ro", "Ro"), 
        ("do", "Do"), 
        ("technicalofficer", "Technicalofficer"), 
        ("bm", "Bm"),
        ("md", "MD"),
        ("cluster", "Cluster")
    ]
    username =  models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=250, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    otp = models.IntegerField(validators=[validate_otp_length], null=True, blank=True)
    bank_branch = models.ForeignKey(BankDetails, on_delete=models.DO_NOTHING)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        UserModel = get_user_model()
        if not self.username:
            self.username = self.email.split("@")[0]

            try:
                UserModel.objects.get(username=self.username)
                self.username = generate_random_string()
            except Exception:
                pass

        super().save(*args, **kwargs)

    class Meta:
        db_table = "User"