from rest_framework import serializers
from .models import CustomerDetails, CustomerAddress

class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'

class CustomCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['uuid', 'cif_id', 'firstName']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'