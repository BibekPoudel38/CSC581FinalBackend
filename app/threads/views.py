from django.shortcuts import render
from .models import Thread, Comment, Categories
from .serializers import ThreadSerializer, CommentSerializer, CategoriesSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count
# import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create and List Threads in class view

class ThreadView(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = ThreadSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def list(self, request, *args, **kwargs):
        queryset = Thread.objects.annotate(comment_count=Count('comment'))
        serializer = ThreadSerializer(queryset, many=True)
        return Response(serializer.data)



# Get the comments according to the thread id from url
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    # In the list function, we need to send the count of replys in the comment 
    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(thread=self.kwargs['thread_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

class NestedComments(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(parent_comment=self.kwargs['comment_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)