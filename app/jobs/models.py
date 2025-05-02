from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

User = get_user_model()


class JobPost(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("closed", "Closed"),
    ]

    JOB_TYPES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    ]

    LEVEL_CHOICES = [
        ("Entry", "Entry"),
        ("Mid", "Mid"),
        ("Senior", "Senior"),
    ]

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_posts"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="job_images/", blank=True, null=True)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    salary_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    salary_unit = models.CharField(
        max_length=10,
        choices=[("hour", "Per Hour"), ("week", "Per Week"), ("month", "Per Month")],
        blank=True,
        null=True,
    )

    type = models.CharField(max_length=50, choices=JOB_TYPES, blank=True, null=True)
    level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, blank=True, null=True
    )
    apply_link = models.URLField(blank=True, null=True)

    category = models.CharField(max_length=100, blank=True, null=True)
    tags = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Add keywords like 'remote', 'part-time', etc.",
    )

    description = models.JSONField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    expiry_date = models.DateField(null=True, blank=True)

    marked_unavailable_by = models.ManyToManyField(
        User, blank=True, related_name="unavailable_jobs"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.expiry_date and timezone.now().date() > self.expiry_date

    def mark_unavailable(self, user):
        self.marked_unavailable_by.add(user)
        if self.marked_unavailable_by.count() >= 5:
            self.status = "closed"
            self.save()

    def __str__(self):
        return self.title
