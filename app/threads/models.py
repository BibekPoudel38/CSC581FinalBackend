from django.db import models
from authentication.models import User


# Create your models here.
class Thread(models.Model):
    title = models.TextField()
    content = models.TextField()
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    view_count = models.IntegerField(default=0)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comment")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

