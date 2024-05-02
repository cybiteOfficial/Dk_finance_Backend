from rest_framework import serializers
from .models import CustomerDetails

class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(CustomerDetailsSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation
