# your_app/auth_backend.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests

SUPABASE_URL = "https://yejfdrifxseujhkxabbm.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllamZkcmlmeHNldWpoa3hhYmJtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg5NTc5NTMsImV4cCI6MjA1NDUzMzk1M30._7zqQE3kstfdnKYHFinuzs5Ym6DLQavdbJpm8sd-go0"


class SupabaseUser:
    """A minimal user-like object for Supabase-authenticated users"""

    def __init__(self, user_data):
        self.id = user_data.get("id")
        self.email = user_data.get("email")
        self.user_metadata = user_data.get("user_metadata")
        self.is_authenticated = True
        self.is_anonymous = False  # ✅ Required by Django internals

    def __str__(self):
        return self.email or "Unknown Supabase User"


class SupabaseAuthentication(BaseAuthentication):
    """Custom JWT-based authentication using Supabase"""

    def enforce_csrf(self, request):
        # ✅ Bypass CSRF check (since we're using token auth)
        return

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Not our responsibility; try next auth backend

        token = auth_header.split(" ")[1]
        print("🔑 Supabase token received:", token)

        user_data = self.verify_supabase_token(token)
        if not user_data:
            raise AuthenticationFailed("Invalid or expired Supabase token")

        user = SupabaseUser(user_data)
        print("👤 Authenticated Supabase user:", user.email)
        return (user, None)

    def verify_supabase_token(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "apikey": SUPABASE_API_KEY,
        }

        try:
            response = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
            print("📬 Supabase response:", response.status_code)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print("❌ Supabase request error:", str(e))
        return None
