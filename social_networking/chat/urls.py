from django.urls import path
from .views import (
    CreateChatRoomAPIView
)

urlpatterns = [
    path("createChatRoom/", CreateChatRoomAPIView.as_view(), name="create-chat-room")
]
