from rest_framework import serializers
from user_auth.models import User, Comments
from django.contrib.auth.models import Group, Permission

from utils import generate_empID


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions", "is_staff", "is_active", "is_superuser"]

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        representation['bank_branch'] = instance.bank_branch.bank_name
        return representation

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "password",
            "confirm_password",
            "email",
            "user_type",
            "emp_id",
            "date_of_birth",
            "phone_number",
            "first_name",
            "last_name",
            "profile_picture",
            "bank_branch",
            "gender",
        ]

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data['emp_id'] = generate_empID()
        user = User.objects.create_user(**validated_data)
        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
    