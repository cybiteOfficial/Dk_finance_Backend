from rest_framework import serializers
from .models import CollateralDetails

class CollateralDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollateralDetails
        fields = '__all__'
    def to_representation(self, instance):
        representation = super(CollateralDetailsSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        return representation