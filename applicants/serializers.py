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
        representation['lead'] = instance.lead.lead_id
        representation['paymentedetails'] = instance.paymentedetails.payment_id
        return representation
    
