
from rest_framework import serializers
from .models import Customer_Caf, DocumentDetail, UploadDocument,Photograph_upload

class Customer_CafSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Caf
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(Customer_CafSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation
    


class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:  
        model = DocumentDetail
        # fields of multiple rows
        fields = ['doc_id', 'doc_image']

class UploadDocumentSerializer(serializers.ModelSerializer):
    details = DocumentDetailSerializer(many=True, read_only=True)  
    class Meta:
        model = UploadDocument
        # static feilds of model
        fields = ['id', 'name', 'details']


class Photograph_uploadSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Photograph_upload
        fields = '__all__'


