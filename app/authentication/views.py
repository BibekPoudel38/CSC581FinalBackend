from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, LoginSerializer, OTPSerializer
from django.core.mail import send_mail
import random
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class SignupView(views.APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_code = str(random.randint(100000, 999999))
            user.otp = otp_code
            user.save()

            # Send email with OTP code
            send_mail(
                "OTP Verification",
                f"Your OTP code is {otp_code}",
                "poudelbibek38@gmail.com",
                [user.email],
            )

            return Response(
                {
                    "message": "Account created. Please verify with the OTP code sent to the email",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(views.APIView):
    def post(self, request):
        otp = request.data.get("otp")
        if not otp:
            return Response(
                {"error": "Please provide OTP code"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = get_user_model().objects.get(otp=otp)
            user.is_active = True
            user.otp = None
            user.save()

            return Response(
                {
                    "message": "Email verified",
                },
                status=status.HTTP_200_OK,
            )

        except get_user_model().DoesNotExist:
            return Response(
                {"error": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(views.APIView):
    def post(self, request):
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")

        try:
            user = get_user_model().objects.get(email=username_or_email)
        except get_user_model().DoesNotExist:
            try:
                user = get_user_model().objects.get(username=username_or_email)
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:
            return Response(
                {"error": "Please verify your email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        user = request.user
        if not user.check_password(old_password):
            return Response(
                {"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed"}, status=status.HTTP_200_OK)


class ForgotPasswordView(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        otp_code = str(random.randint(100000, 999999))
        user.otp = otp_code
        user.save()

        send_mail(
            "OTP Verification",
            f"Your OTP code is {otp_code}",
            "poudelbibek38@gmail.com",
            [user.email],
        )
        
        return Response(
            {"message": "OTP code sent to your email"},
            status=status.HTTP_200_OK,
        )
