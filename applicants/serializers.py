from rest_framework import serializers
from leads.serializers import LeadsSerializer
from phonepay.serializers import PaymentSerializer
from customer.serializers import CustomerDetailsSerializer
from .models import Applicants

class ApplicantsSerializer(serializers.ModelSerializer):
    # lead = LeadsSerializer()
    # paymentedetails = PaymentSerializer()
    # customer = CustomerDetailsSerializer()

    class Meta:
        model = Applicants
        fields = '__all__'