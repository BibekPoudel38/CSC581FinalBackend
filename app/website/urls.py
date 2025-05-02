from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("threads/", views.threads, name="threads"),
    re_path(r"^.*\.*", views.pages, name="pages"),
]
