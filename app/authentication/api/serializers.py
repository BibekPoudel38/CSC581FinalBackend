from rest_framework import serializers
from ..models import User
from django.contrib.auth import authenticate
import validators


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['password',]
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)

                if not user:
                    raise serializers.ValidationError({
                        "message": "Access denied. username no or password didn't match",
                    })

            else:
                raise serializers.ValidationError({
                    "message": "User with the username doesnot exist",
                })
        attrs['user'] = user
        return attrs


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'mobile_no']
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def create(self, validated_data, *args):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({
                "error": "The email number is already in use"
            })
        elif User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({
                "error": "The username number is already in use"
            })
        else:
            print(validated_data['full_name'])
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                mobile_no=validated_data['mobile_no'],
            )
            password = validated_data['password']
            user.set_password(password)
            user.save()
            return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'gender',
                  'is_verified', 'firebase_token']
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password])

    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'old_password']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({
                "error": "Old password is not correct"
            })
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# class ResetPasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validators.validate_password])
#     code = serializers.CharField(write_only=True, required=True)
#     email = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['password', 'code', 'email']

#     def update(self, instance, validated_data):
#         otp_obj = OtpModel.objects.get(
#             email=validated_data['email'])
#         user = User.objects.get(email=otp_obj.email)
#         if otp_obj.code == validated_data['code']:
#             user.set_password(validated_data['password'])
#             user.firebase_token = ""
#             user.save()
#             return instance
#         return None
