from rest_framework import serializers
from .models import CollateralDetails

class CollateralDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollateralDetails
        fields = '__all__'
