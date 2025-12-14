# accounts/tests.py (example)
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username="alice", password="pass")
        self.user_b = User.objects.create_user(username="bob", password="pass")
        self.user_c = User.objects.create_user(username="carol", password="pass")

        # posts by bob and carol
        Post.objects.create(author=self.user_b, title="B1", content="B1")
        Post.objects.create(author=self.user_c, title="C1", content="C1")

    def test_follow_and_feed(self):
        # login as alice
        self.client.login(username="alice", password="pass")

        # follow bob
        follow_url = reverse("accounts:follow", args=[self.user_b.id])
        resp = self.client.post(follow_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # access feed
        feed_url = reverse("feed")
        resp = self.client.get(feed_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # should contain bob's post, not carol's
        titles = [item["title"] for item in resp.data["results"]]
        self.assertIn("B1", titles)
        self.assertNotIn("C1", titles)
