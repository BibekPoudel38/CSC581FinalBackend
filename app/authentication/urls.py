from django.urls import path,include
from .views import login_view
from django.contrib.auth.views import LogoutView
from .api import views as api_views

urlpatterns = [
    path('login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),


    # API Ednpoints
    path('api/login/', api_views.LoginView.as_view(), name="Login View"),
    path('signup/', api_views.SignupView.as_view(), name="Signup View"),
#     path('generate_otp/', api_views.generateOtp, name="OTP Generator View"),
#     path('validate_otp/', api_views.validate_Otp, name="Validate OTP Code"),
#     path('reset_password/', api_views.ResetPassword.as_view(), name="Reset password"),
    path('profile/', api_views.ProfileView.as_view(), name="Profile View"),
    path('profile/update/', api_views.ProfileUpdateView.as_view(),name="Profile Update View"),
    path('change_password/',api_views.ChangePassword.as_view(), name="Change Password"),
]
