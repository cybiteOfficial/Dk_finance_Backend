from rest_framework import serializers
from leads.serializers import LeadsSerializer
from phonepay.serializers import PaymentSerializer
from customer.serializers import CustomerDetailsSerializer
from .models import Applicants

class ApplicantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicants
        fields = '__all__'
    

    def to_representation(self, instance):
        representation = super(ApplicantsSerializer, self).to_representation(instance)
        if instance.lead:
            representation['lead'] = instance.lead.lead_id
        representation['paymentedetails'] = instance.paymentedetails.payment_id
        if instance.comment:
            representation['comment'] = instance.comment.comment
        representation['created_by'] = {
            'ro_name': instance.created_by.username,
            'employee_id': instance.created_by.emp_id,
        }
        return representation
