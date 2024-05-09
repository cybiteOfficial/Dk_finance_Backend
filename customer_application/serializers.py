from rest_framework import serializers
from .models import CustomerApplicationForm

class CafSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerApplicationForm
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(CafSerializer, self).to_representation(instance)
        if instance.comment:    
            representation['comment'] = instance.comment.comment
        if instance.applicant is not None:
            representation['applicant'] = instance.applicant.application_id
        if instance.pdWith is not None:
            representation['pdWith'] = instance.pdWith.cif_id
        return representation