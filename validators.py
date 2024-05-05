from django.core.exceptions import ValidationError
import phonenumbers
from email_validator import validate_email


def validate_otp_length(value):
    if not (100000 <= value <= 999999):
        raise ValidationError("OTP must be exactly 6 digits.")


def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value)
        phonenumbers.is_valid_number(phone_number)
        return True
    except Exception:
        return False


def validate_email(value):
    try:
        validate_email(value)
        return True
    except Exception:
        return False
