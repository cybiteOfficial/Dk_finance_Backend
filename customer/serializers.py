from rest_framework import serializers
from .models import CustomerDetails, CustomerAddress

class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(CustomerDetailsSerializer, self).to_representation(instance)
        if instance.applicant:
            representation['applicant'] = instance.applicant.application_id
        return representation

class CustomCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['uuid', 'cif_id', 'firstName']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            'uuid',
            'address_line_1',
            'address_line_2',
            'address_line_3',
            'state',
            'city',
            'district',
            'tehsil_or_taluka',
            'pincode',
            'landmark',
            'residence_state',
            'residence_type',
            'stability_at_residence',
            'distance_from_branch'
        ]
        
    def to_representation(self, instance):
        representation = super(AddressSerializer, self).to_representation(instance)
        if instance.customer:
            representation['customer'] = instance.customer.cif_id
        return representation
