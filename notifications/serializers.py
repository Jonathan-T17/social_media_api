# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    recipient_username = serializers.CharField(source="recipient.username", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "recipient", "recipient_username", "actor", "actor_username",
                  "verb", "target_content_type", "target_object_id", "created_at", "unread"]
        read_only_fields = ["id", "created_at", "actor", "recipient", "actor_username", "recipient_username"]
