# Create models here.
# notifications/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="actor_notifications", on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  # e.g., "liked", "commented on", "followed you"
    # Generic target (optional) so notifications can point to Post/Comment/User/Like etc.
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")
    timestamp = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_read(self):
        if self.unread:
            self.unread = False
            self.save(update_fields=["unread"])
