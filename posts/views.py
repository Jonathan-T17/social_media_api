# Create views here.
# posts/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from notifications.utils import create_notification
from rest_framework import generics
from notifications.models import Notification




User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    base_queryset = Post.objects.all()

    queryset = Post.objects.select_related("author").prefetch_related("comments").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__username", "created_at", "updated_at"]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "title", "updated_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # extra action to list comments for a post via /posts/{pk}/comments/
    @action(detail=True, methods=["get"], url_path="comments", permission_classes=[permissions.AllowAny])
    def list_comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
    

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated], url_path="like")
    def like(self, request, pk=None):
        # Required explicit usage:
        post = generics.get_object_or_404(Post, pk=pk)

        user = request.user

        try:
            with transaction.atomic():
                # Required explicit usage:
                like, created = Like.objects.get_or_create(user=request.user, post=post)

                if created:
                    # Required explicit usage:
                    # Even if you're using signals, we include this safely:
                    if post.author != user:
                        Notification.objects.create(
                            recipient=post.author,
                            actor=user,
                            verb="liked your post",
                            target=post
                        )

                    serializer = LikeSerializer(like, context={"request": request})
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

        except IntegrityError:
            return Response({"detail": "Could not like post."}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated], url_path="unlike")
    def unlike(self, request, pk=None):
        # Use the required call here too
        post = generics.get_object_or_404(Post, pk=pk)

        user = request.user
        deleted, _ = Like.objects.filter(post=post, user=user).delete()

        if deleted:
            return Response({"detail": "Unliked."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    base_queryset = Comment.objects.all()

    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["post", "author__username", "created_at"]
    search_fields = ["content", "author__username"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def perform_create(self, serializer):
        # if post is passed by body: serializer.validated_data['post'] will hold it; otherwise, prefer URL param.
        post = serializer.validated_data.get("post", None)
        if post is None and "post_id" in self.request.parser_context.get("kwargs", {}):
            # not common; fallback
            post_id = self.request.parser_context["kwargs"]["post_id"]
            post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)




class UserFeedView(ListAPIView):
    """
    Returns posts authored by users the current user follows,
    ordered by newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # reuse existing pagination

    def get_queryset(self):
        user = self.request.user
        # If user follows no one, return empty queryset
        following_users = user.following.all()
        feed_posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        return feed_posts.select_related("author").prefetch_related("comments")