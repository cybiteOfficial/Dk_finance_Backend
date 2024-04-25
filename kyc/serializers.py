from rest_framework import serializers
from .models import KYCDetails, DocumentsUpload

class KycDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = KYCDetails
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super(KycDetailsSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation

class DocumentUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentsUpload
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(DocumentUploadSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation