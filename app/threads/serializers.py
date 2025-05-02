from .models import Thread, Comment, Categories, ThreadVote, CommentVote
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    comment_count = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all(),
        many=True,
        required=True,
    )
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "content",
            "file",
            "user",
            "view_count",
            "up_vote",
            "down_vote",
            "user_vote",
            "category",
            "created_at",
            "updated_at",
            "comment_count",
        ]
        read_only_fields = ["view_count", "up_vote", "down_vote"]

    def get_up_vote(self, obj):
        return ThreadVote.objects.filter(thread=obj, vote_type="upvote").count()

    def get_down_vote(self, obj):
        return ThreadVote.objects.filter(thread=obj, vote_type="downvote").count()

    def get_user_vote(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                vote = ThreadVote.objects.get(thread=obj, user=request.user)
                return vote.vote_type
            except ThreadVote.DoesNotExist:
                return None
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = instance.user
        data["user"] = {
            "id": user.id,
            "email": user.email,
        }
        # Add category names to the response
        categories = instance.category.all()
        data["category"] = [
            {"id": category.id, "name": category.name} for category in categories
        ]
        return data


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.IntegerField(read_only=True)
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "thread",
            "parent_comment",
            "user",
            "reply_count",
            "up_vote",
            "down_vote",
            "user_vote",
            "created_at",
            "updated_at",
        ]

    read_only_fields = ["up_vote", "down_vote", "user"]

    def get_up_vote(self, obj):
        return CommentVote.objects.filter(comment=obj, vote_type="upvote").count()

    def get_down_vote(self, obj):
        return CommentVote.objects.filter(comment=obj, vote_type="downvote").count()

    def get_user_vote(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                vote = CommentVote.objects.get(comment=obj, user=request.user)
                return vote.vote_type
            except CommentVote.DoesNotExist:
                return None
        return None


class NestedCommentsSerializer(serializers.ModelSerializer):
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
