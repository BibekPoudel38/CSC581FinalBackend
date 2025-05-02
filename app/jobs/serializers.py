from rest_framework import serializers
from .models import JobPost
from django.utils import timezone


class JobPostSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.id")
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    is_expired = serializers.SerializerMethodField()
    marked_unavailable_by_count = serializers.SerializerMethodField()

    class Meta:
        model = JobPost
        fields = "__all__"

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_marked_unavailable_by_count(self, obj):
        return obj.marked_unavailable_by.count()

    def validate_expiry_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Expiry date cannot be in the past.")
        if value and (value - timezone.now().date()).days > 60:
            raise serializers.ValidationError(
                "Expiry date can't be more than 60 days in the future."
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["creator"] = user
        job = JobPost.objects.create(**validated_data)
        return job

    def update(self, instance, validated_data):
        # Prevent users from changing creator or status
        validated_data.pop("creator", None)
        validated_data.pop("status", None)
        return super().update(instance, validated_data)
