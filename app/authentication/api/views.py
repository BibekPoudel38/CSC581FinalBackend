from rest_framework import views, permissions
from .serializers import LoginSerializer, SignupSerializer, ProfileSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from ..models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import email_handler as emailHandler
from base.permissions import IsVerifiedUser
from rest_framework.decorators import api_view
# Create your views here.


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            jwt_token = RefreshToken.for_user(user)
            user.save()
            return Response(
                {
                    'status': True,
                    'refresh': str(jwt_token),
                    'access': str(jwt_token.access_token)
                }, 
                status=status.HTTP_200_OK,
            )


class SignupView(GenericAPIView, CreateModelMixin):
    serializer_class = SignupSerializer

    def post(self, requset, **kwargs):
        serializer = self.serializer_class(data=requset.data)
        if serializer.is_valid():
            user = serializer.create(requset.data, **kwargs)
            if (user):
                sendOTPCode(user.email)
                jwt_token = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'message': "Account created",
                    'refresh': str(jwt_token),
                    'access': str(jwt_token.access_token)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': False,
                    'message': "Unable to create account",
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "status": False,
                    'errors': serializer.errors,
                }, 
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user, context={'request': request})
        return Response(
            {
                "profile": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileUpdateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print(data)
        serializer = ProfileSerializer(
            data=data, instance=user
        )
        if (serializer.is_valid()):
            serializer.save()
            return Response(
                {
                    "status": True,
                }, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                "status": False,
                "error": serializer.errors,
                }
            )