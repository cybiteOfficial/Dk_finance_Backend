from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  
    def to_representation(self, instance):
        representation = super(PaymentSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation
