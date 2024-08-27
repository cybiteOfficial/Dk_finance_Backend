from django.db import models
from user_auth.models import BaseModel, User
from applicants.models import Applicants

class ErrorLog(BaseModel):
    error_type = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    pathname = models.CharField(max_length=1024)
    lineno = models.IntegerField()
    funcName = models.CharField(max_length=255)
    error_message = models.TextField()
    
    
class UserLog(BaseModel):
    
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    api = models.CharField(max_length=255)
    details = models.CharField(max_length=255, null=True, blank=True)
    applicant = models.ForeignKey(Applicants, on_delete=models.DO_NOTHING ,null=True)
    