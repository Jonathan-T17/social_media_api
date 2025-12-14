# posts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like
from notifications.utils import create_notification

@receiver(post_save, sender=Like)
def like_created_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.user
        recipient = post.author
        if recipient != actor:
            # create notification: "user liked your post"
            create_notification(recipient=recipient, actor=actor, verb="liked your post", target=post)

@receiver(post_delete, sender=Like)
def like_deleted_notification(sender, instance, **kwargs):
    # Optionally, you might create a "unliked" notification or simply ignore deletes.
    pass
