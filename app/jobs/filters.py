import django_filters
from .models import JobPost
from django.utils import timezone
from django.db import models


class JobPostFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="salary_amount", lookup_expr="gte"
    )
    max_salary = django_filters.NumberFilter(
        field_name="salary_amount", lookup_expr="lte"
    )
    tags = django_filters.CharFilter(method="filter_tags")
    is_expired = django_filters.BooleanFilter(method="filter_expired")

    # NEW ADDED FILTERS
    type = django_filters.CharFilter(field_name="type", lookup_expr="iexact")
    level = django_filters.CharFilter(field_name="level", lookup_expr="iexact")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="category", lookup_expr="icontains")

    class Meta:
        model = JobPost
        fields = [
            "category",
            "status",
            "type",
            "level",
            "location",
            "min_salary",
            "max_salary",
            "tags",
            "is_expired",
        ]

    def filter_tags(self, queryset, name, value):
        tag_list = value.split(",")
        return queryset.filter(tags__overlap=tag_list)

    def filter_expired(self, queryset, name, value):
        today = timezone.now().date()
        if value:  # Only expired
            return queryset.filter(expiry_date__lt=today)
        else:  # Only active
            return queryset.filter(
                models.Q(expiry_date__gte=today) | models.Q(expiry_date__isnull=True)
            )
