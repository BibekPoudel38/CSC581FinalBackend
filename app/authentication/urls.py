from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views as api_views

urlpatterns = [
    # API Ednpoints
    path('api/signup/', api_views.SignupView.as_view(), name='signup'),
    path('api/verify-otp/', api_views.VerifyOTPView.as_view(), name='verify-otp'),
    path('api/login/', api_views.LoginView.as_view(), name='login'),
    path('api/change-password/', api_views.ChangePasswordView.as_view(), name='change-password'),
    path('api/forgot-password/', api_views.ForgotPasswordView.as_view(), name='forgot-password'),
]
