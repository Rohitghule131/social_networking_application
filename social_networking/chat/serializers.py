from rest_framework import serializers

from .models import (
    Messages,
    ChatConnection
)


class CreateChatConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer class for create chat room.
    """
    class Meta:
        fields = ("id", "chat_room", "users", "created_at", "updated_at")
        model = ChatConnection

