from rest_framework import serializers
from .models import Customer_Caf

class Customer_CafSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Caf
        fields = '__all__'
