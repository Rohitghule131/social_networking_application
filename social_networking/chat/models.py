from django.db import models
from uuid import uuid4

from users.models import CustomUser
from utilities.constant import LINK_TYPE
from utilities.mixins import CustomMixins


class ChatConnection(CustomMixins):
    """
    Class for create a chat connection between the users.
    """
    chat_room = models.CharField(max_length=200, null=False, blank=False, default=uuid4())
    users = models.ManyToManyField(CustomUser, related_name="chat_between_users")


class Messages(CustomMixins):
    """
    Class for create a Messages model to chat messages between the users.
    """
    messages = models.TextField(null=False, blank=False)
    chat_room_connection = models.ForeignKey(ChatConnection, null=False, blank=False, on_delete=models.CASCADE)
    link = models.URLField(null=True, blank=False)
    link_type = models.CharField(max_length=50, null=True, blank=False, choices=LINK_TYPE)
    send_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
