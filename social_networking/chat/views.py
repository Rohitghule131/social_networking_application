from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from utilities.utils import (
    ResponseInfo,
)
from utilities import messages
from .models import ChatConnection
from .serializers import (
    CreateChatConnectionSerializer
)


class CreateChatRoomAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CreateChatConnectionSerializer

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(CreateChatRoomAPIView, self).__init__(**kwargs)

    def get_queryset(self):
        """
        Method to return the chat connection.
        """
        return ChatConnection.objects.filter(users__in=[self.request.user.id]).first()

    def post(self, request, *args, **kwargs):
        """
        POST method to create a room for users.
        """
        chat_connection_object = self.get_queryset()

        if chat_connection_object:
            chat_connection_serializer = self.get_serializer(chat_connection_object)
            self.response_format["data"] = chat_connection_serializer.data
            self.response_format["message"] = messages.FETCHED_SUCCESS.format("Chat room")
            self.response_format["status_code"] = status.HTTP_200_OK

        else:
            create_chat_room = super().post(request, *args, **kwargs)
            self.response_format["data"] = create_chat_room.data
            self.response_format["message"] = messages.CREATED_SUCCESSFULLY.format("Chat room created")
            self.response_format["status_code"] = status.HTTP_201_CREATED

        return Response(self.response_format, status=self.response_format.get("status_code"))

