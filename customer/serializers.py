from rest_framework import serializers
from .models import CustomerDetails, CustomerAddress, CustomerKYCDetails

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
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super(AddressSerializer, self).to_representation(instance)
        if instance.customer:
            representation['customer'] = instance.customer.cif_id
        return representation

class KYCSDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerKYCDetails
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super(KYCSDetailsSerializer, self).to_representation(instance)
        if instance.customer:
            representation['customer'] = instance.customer.cif_id
        return representation
