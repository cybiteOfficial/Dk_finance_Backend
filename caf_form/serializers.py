from rest_framework import serializers
from .models import CafDetails

class CafSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafDetails
        fields = '__all__'
