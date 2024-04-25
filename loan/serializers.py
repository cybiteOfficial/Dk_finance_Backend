from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(LoanSerializer, self).to_representation(instance)
        representation['applicant'] = instance.applicant.application_id
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation