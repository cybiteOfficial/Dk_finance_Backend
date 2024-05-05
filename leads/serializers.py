from rest_framework import serializers
from user_auth.models import User
from .models import Leads

class LeadsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leads
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super(LeadsSerializer, self).to_representation(instance)
        if instance.comment:
            representation['comment'] = instance.comment.comment
        if instance.assigned_to is not None:
            representation['assigned_to'] = instance.assigned_to.email
        return representation