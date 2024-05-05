from django.db import models
from choices import Choices
from applicants.models import Applicants
from utils import generate_cafID, generate_photoID
from user_auth.models import Comments, BaseModel

class Customer_Caf(BaseModel):
    caf_id = models.CharField(max_length=255, default=generate_cafID, unique=True)
    applicant = models.OneToOneField(Applicants, on_delete=models.CASCADE, related_name='applicant_id', null=True)
    
    tentative_amt = models.FloatField(max_length=15, null=True, blank=True)
    pdWith = models.CharField(max_length=255, null=True, blank=True)
    placeOfPdAddress = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)
    



class UploadDocument(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    applicant = models.ForeignKey(Applicants, related_name='uploaded_documents', on_delete=models.CASCADE)

class DocumentDetail(models.Model):
    upload_document = models.ForeignKey(UploadDocument, related_name='details', on_delete=models.CASCADE)
    doc_id = models.CharField(max_length=50, blank=True, null=True)
    doc_image = models.ImageField(upload_to='documents_images/', blank=True, null=True)
    applicant = models.ForeignKey(Applicants, related_name='document_details', on_delete=models.CASCADE)



class Photograph_upload(BaseModel):
    photo_id = models.CharField(max_length=255, default=generate_photoID, unique=True)
    applicant = models.OneToOneField(Applicants, on_delete=models.CASCADE, related_name='applicantphoto_id', null=True)
    photograph = models.ImageField(upload_to='photograph_images/', blank=True, null=True)
    description = models.TextField(null=True)
    comment = models.ForeignKey(Comments, on_delete=models.DO_NOTHING, null=True)

