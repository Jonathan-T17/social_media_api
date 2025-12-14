from django.test import TestCase

# Create  tests here.
# posts/tests.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment

User = get_user_model()

class PostCommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        self.post = Post.objects.create(author=self.user, title="Test Post", content="Body")
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Nice")

    def test_list_posts(self):
        url = reverse("post-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data["results"]) >= 1)

    def test_create_post_requires_auth(self):
        url = reverse("post-list")
        data = {"title": "New", "content": "New body"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # login then create
        self.client.login(username="user1", password="pass123")
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_update_post_only_owner(self):
        url = reverse("post-detail", args=[self.post.id])
        self.client.login(username="user2", password="pass123")
        resp = self.client.put(url, {"title": "X", "content": "Y"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        self.client.login(username="user1", password="pass123")
        resp = self.client.put(url, {"title": "Updated", "content": "Updated body"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        url = reverse("comment-list")
        self.client.login(username="user2", password="pass123")
        resp = self.client.post(url, {"post": self.post.id, "content": "Great!"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)



