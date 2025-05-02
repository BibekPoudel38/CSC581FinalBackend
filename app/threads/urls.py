from django.urls import path
from .views import (
    ThreadView,
    CategoryView,
    CommentView,
    NestedComments,
    ThreadVoteView,
    CommentVoteView,
)

urlpatterns = [
    # Threads
    path(
        "",
        ThreadView.as_view({"get": "list", "post": "create"}),
        name="threads",
    ),
    path(
        "<int:pk>/",
        ThreadView.as_view({"get": "retrieve"}),
        name="thread-retrieve",
    ),
    # Categories
    path("categories/", CategoryView.as_view({"get": "list"}), name="categories"),
    # Comments
    path(
        "<int:thread_id>/comments/",
        CommentView.as_view({"get": "list", "post": "create"}),
        name="comments",
    ),
    path(
        "<int:thread_id>/comments/<int:comment_id>/",
        NestedComments.as_view({"get": "list", "post": "create"}),
        name="nested-comments",
    ),
    # Votes
    path(
        "<int:pk>/<str:action>/",
        ThreadVoteView.as_view({"post": "create"}),
        name="thread-vote",
    ),
    path(
        "comments/<int:pk>/<str:action>/",
        CommentVoteView.as_view({"post": "create"}),
        name="comment-vote",
    ),
]
