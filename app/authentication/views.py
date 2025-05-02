from rest_framework import views, permissions
from .serializers import LoginSerializer, SignupSerializer, ProfileSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random

# views.py
from rest_framework.views import APIView
import requests
from django.views.decorators.csrf import csrf_exempt

# import email_handler as emailHandler
# from base.permissions import IsVerifiedUser
from rest_framework.decorators import api_view

# Create your views here.


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            jwt_token = RefreshToken.for_user(user)
            user.save()
            return Response(
                {
                    "refresh": str(jwt_token),
                    "access": str(jwt_token.access_token),
                },
                status=status.HTTP_200_OK,
            )


class SignupView(GenericAPIView, CreateModelMixin):
    serializer_class = SignupSerializer

    def post(self, requset, **kwargs):
        serializer = self.serializer_class(data=requset.data)
        if serializer.is_valid():
            user = serializer.create(requset.data, **kwargs)
            if user:
                # sendOTPCode(user.email)
                jwt_token = RefreshToken.for_user(user)
                return Response(
                    {
                        "status": True,
                        "message": "Account created",
                        "refresh": str(jwt_token),
                        "access": str(jwt_token.access_token),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "Unable to create account",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user, context={"request": request})
        return Response(
            {
                "profile": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileUpdateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print(data)
        serializer = ProfileSerializer(data=data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": False,
                    "error": serializer.errors,
                }
            )


class ChangePassword(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        user = request.user
        if not user.check_password(old_password):
            return Response(
                {
                    "status": False,
                    "message": "Old password is incorrect",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {
                "status": True,
                "message": "Password changed successfully",
            },
            status=status.HTTP_200_OK,
        )


# When the user asks for reset password, send the email with the OTP Code to reset the password
@api_view(["POST"])
def send_reset_password_otp(request):
    email = request.data["email"]
    user = User.objects.filter(email=email).first()
    if user:
        otp = random.randint(100000, 999999)
        # emailHandler.send_otp(email, otp)
        user.otp = otp
        print(otp)
        user.save()
        return Response(
            {
                "status": True,
                "message": "OTP sent to your email",
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": False,
                "message": "User with the email doesnot exist",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Now when the user sends the otp code, check if the otp is correct
# cors exception
@csrf_exempt
@api_view(["POST"])
def verify_reset_password_otp(request):
    email = request.data["email"]
    otp = request.data["otp"]
    user = User.objects.filter(email=email).first()
    if user.otp == otp:
        return Response(
            {
                "status": True,
                "message": "OTP is correct",
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": False,
                "message": "OTP is incorrect",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Now when the user sends the new password, check if the otp is correct and update the password
@csrf_exempt
@api_view(["POST"])
def reset_password(request):
    email = request.data["email"]
    otp = request.data["otp"]
    password = request.data["password"]
    user = User.objects.filter(email=email, otp=otp).first()
    if not user:
        return Response(
            {
                "status": False,
                "message": "OTP is incorrect",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.set_password(password)
    user.save()
    return Response(
        {
            "status": True,
            "message": "Password reset successfully",
        },
        status=status.HTTP_200_OK,
    )


class GoogleLoginAPIView(APIView):

    def post(self, request, format=None):
        print("here")
        id_token = request.data.get("token")

        if id_token is None:
            return Response(
                {"error": "Token missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verify the token
        google_verify_url = (
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        )
        response = requests.get(google_verify_url)
        if response.status_code != 200:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_info = response.json()
        email = user_info["email"]
        name = user_info.get("name", "")

        # Find or create user
        user, created = User.objects.get_or_create(
            email=email, defaults={"username": email.split("@")[0], "first_name": name}
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
