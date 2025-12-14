from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikesNotificationsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="u1", password="pass1")
        self.user2 = User.objects.create_user(username="u2", password="pass2")
        self.post = Post.objects.create(author=self.user2, title="T", content="C")

    def test_like_creates_notification(self):
        self.client.force_authenticate(self.user1)
        url = f"/api/posts/{self.post.pk}/like/"
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        # Check Like exists
        liked = Like.objects.filter(post=self.post, user=self.user1).exists()
        self.assertTrue(liked)
        # Check notification for post.author (user2)
        notif = Notification.objects.filter(recipient=self.user2, actor=self.user1, verb__icontains="like").exists()
        self.assertTrue(notif)

    def test_unlike_removes_like(self):
        Like.objects.create(post=self.post, user=self.user1)
        self.client.force_authenticate(self.user1)
        url = f"/api/posts/{self.post.pk}/unlike/"
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Like.objects.filter(post=self.post, user=self.user1).exists())
