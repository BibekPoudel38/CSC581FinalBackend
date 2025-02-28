from django.urls import path, include
from .views import ThreadView

urlpatterns = [
    # API Ednpoints
    # Get and Post Threads
    path('api/threads/', ThreadView.as_view({'get': 'list', 'post': 'create'}), name='threads'),
]
