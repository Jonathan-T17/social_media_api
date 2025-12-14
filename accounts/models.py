from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="user_following",
        blank=True
    )

    # Users that THIS user follows
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="user_followers",
        blank=True,
        help_text="Users this user follows (asymmetric relationship)."
    )

    def __str__(self):
        return self.username
