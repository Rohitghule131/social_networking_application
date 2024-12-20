from django.urls import path

from .views import (
    ListUsersAPIView,
    LoginUserAPIView,
    SignUpUserAPIView,
    ListFriendUsersAPIView,UserDetailsAPIView,
    FriendRequestActionAPIView,
    ListPendingFriendRequestAPIView
)

urlpatterns = [
    path("login", LoginUserAPIView.as_view(), name="login"),
    path("signUp", SignUpUserAPIView.as_view(), name="sign-up"),
    path("userDetails", UserDetailsAPIView.as_view(), name="user-detials"),

    path("listUsers", ListUsersAPIView.as_view(), name="users-list"),
    path("listFriendUsers", ListFriendUsersAPIView.as_view(), name="list-friend-users"),
    path("listPendingFriendsRequest", ListPendingFriendRequestAPIView.as_view(), name="list-pending-friends-request"),

    path("friendRequestAction", FriendRequestActionAPIView.as_view(), name="friend-request-action")
]
