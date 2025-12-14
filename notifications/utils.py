# notifications/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Create a notification for recipient.
    target can be a model instance (Post, Comment, User, Like, etc.) or None.
    """
    kwargs = {
        "recipient": recipient,
        "actor": actor,
        "verb": verb,
    }
    if target is not None:
        kwargs["target_content_type"] = ContentType.objects.get_for_model(target)
        kwargs["target_object_id"] = str(target.pk)
    return Notification.objects.create(**kwargs)
