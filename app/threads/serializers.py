from .models import Thread, Comment, Categories
from rest_framework import serializers

class ThreadSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'file', 'user', 'view_count', 'up_vote', 'down_vote', 'created_at', 'updated_at', 'comment_count']
        read_only_fields = ["view_count", "up_vote", "down_vote"]
        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        

class CategoriesSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Categories
        fields = "__all__"