from rest_framework import serializers
from .models import KYCDetails, DocumentsUpload

class KycDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = KYCDetails
        fields = "__all__"
    
    # def to_representation(self, instance):
    #     representation = super(KycDetailsSerializer, self).to_representation(instance)
    #     representation['lead'] = instance.lead.lead_id
    #     return representation

class DocumentUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentsUpload
        fields = '__all__'