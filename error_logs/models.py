from django.db import models
from user_auth.models import BaseModel

class ErrorLog(BaseModel):
    error_type = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    pathname = models.CharField(max_length=1024)
    lineno = models.IntegerField()
    funcName = models.CharField(max_length=255)
    error_message = models.TextField()
    