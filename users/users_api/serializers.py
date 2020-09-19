"""
Serializers for user login and signup
"""
from rest_framework import serializers
from ..models import Users, ProfileImage


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['profile_image',]


class SignUpSerializer(serializers.ModelSerializer):
    """
        Signup information serializer.
    """
    class Meta:
        """
            Define model and fields for serializer.
        """
        model = Users
        fields = ('full_name', 'email', 'mobile', 'password')


class LoginSerializer(serializers.ModelSerializer):
    """
        Login serializer for user login.
    """
    class Meta:
        """
            Define model and fields for serializer.
        """
        model = Users
        fields = ('user_id', 'full_name', 'email', 'mobile')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_id", "full_name", "phone_number", "email", "profile_image", "date_of_birth", "ssn",
                  "zipcode", "state", "address"]


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["full_name", "phone_number", "email", "profile_image", "date_of_birth", "ssn",
                  "zipcode", "state", "address"]
        read_only_fields = ["date_of_birth", "phone_number", "email"]