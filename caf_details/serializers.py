from rest_framework import serializers
from .models import Customer_Caf

class Customer_CafSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Caf
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(Customer_CafSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation
