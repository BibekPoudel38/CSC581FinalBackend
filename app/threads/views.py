from django.shortcuts import render
from .models import Thread, Comment, Categories, ThreadVote, CommentVote
from .serializers import ThreadSerializer, CommentSerializer, CategoriesSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.views import APIView
from django.db.models import Count, Q
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework import status

# Create and List Threads in class view


class ThreadView(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = ThreadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def list(self, request, *args, **kwargs):
        cat_ids = request.query_params.getlist("cat")
        search_query = request.query_params.get("q")

        queryset = Thread.objects.annotate(
            comment_count=Count("comment", distinct=True)
        )

        if cat_ids:
            queryset = queryset.filter(category__id__in=cat_ids)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        queryset = queryset.distinct().order_by("-created_at")

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
        queryset = Comment.objects.filter(thread=self.kwargs["thread_id"])
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
        queryset = Comment.objects.filter(parent_comment=self.kwargs["comment_id"])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # Important if your global auth is enforced!

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name="dispatch")
class ThreadVoteView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, pk, action):
        thread = Thread.objects.get(pk=pk)
        user = request.user

        try:
            existing_vote = ThreadVote.objects.get(user=user, thread=thread)

            if existing_vote.vote_type == action:
                existing_vote.delete()
                return Response(
                    {"message": f"Vote {action}d successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            # If user voted differently before, update their vote
            existing_vote.vote_type = action
            existing_vote.save()
            return Response(
                {"message": f"Vote updated to {action}."}, status=status.HTTP_200_OK
            )

        except ThreadVote.DoesNotExist:
            # No previous vote, create one
            ThreadVote.objects.create(user=user, thread=thread, vote_type=action)
            return Response(
                {"message": f"Thread {action}d successfully."},
                status=status.HTTP_201_CREATED,
            )


class CommentVoteView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, pk, action):
        comment = Comment.objects.get(pk=pk)
        user = request.user

        try:
            existing_vote = CommentVote.objects.get(user=user, comment=comment)

            if existing_vote.vote_type == action:
                existing_vote.delete()
                return Response(
                    {"message": f"Vote {action}d successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            # If user voted differently before, update their vote
            existing_vote.vote_type = action
            existing_vote.save()
            return Response(
                {"message": f"Vote updated to {action}."}, status=status.HTTP_200_OK
            )

        except CommentVote.DoesNotExist:
            # No previous vote, create one
            CommentVote.objects.create(user=user, comment=comment, vote_type=action)
            return Response(
                {"message": f"Comment {action}d successfully."},
                status=status.HTTP_201_CREATED,
            )
