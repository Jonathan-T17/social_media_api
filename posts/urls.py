# posts/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, UserFeedView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),

    # Explicit endpoints
    path("posts/<int:pk>/like/", PostViewSet.as_view({"post": "like"}), name="post-like"),
    path("posts/<int:pk>/unlike/", PostViewSet.as_view({"post": "unlike"}), name="post-unlike"),

    path("feed/", UserFeedView.as_view(), name="feed"),
]
