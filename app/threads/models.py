from django.db import models
from authentication.models import User


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
class Thread(models.Model):
    title = models.TextField()
    content = models.JSONField()
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    view_count = models.IntegerField(default=0)
    category = models.ManyToManyField(Categories, through="ThreadCategory", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ThreadVote(models.Model):
    VOTE_TYPES = (
        ("upvote", "Upvote"),
        ("downvote", "Downvote"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "thread")  # ⚡ One vote per user per thread


class ThreadCategory(models.Model):
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = (
            "threads_thread_category"  # same as the auto-generated one (optional)
        )


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


class CommentVote(models.Model):
    VOTE_TYPES = (
        ("upvote", "Upvote"),
        ("downvote", "Downvote"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")  # ⚡ One vote per user per thread
