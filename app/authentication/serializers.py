from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    
    def validate_email(self,value):
        if not value.endswith('@toromail.csudh.edu'):
            raise ValidationError("You must use a toromail email address")
        return value
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    
class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    def validate_otp(self, value):
        if len(value) != 6:
            raise ValidationError("OTP must be 6 digits")
        return value


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()