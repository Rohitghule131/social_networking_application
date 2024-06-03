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
    CustomException,
    CustomPagination,
    get_tokens_for_user,
)
from utilities import messages
from .serializers import (
    LoginUserSerializer,
    SignUpUserSerializer,
    UserDetailSerializer,
    FriendRequestSerializer,
    ListFriendRequestSerializer,
    ListPendingFriendRequestSerializer
)
from .models import (
    CustomUser,
    FriendRequests
)


class SignUpUserAPIView(CreateAPIView):
    """
    Class for create an API for sign up the user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SignUpUserSerializer

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(CreateAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST method for create a user.
        """
        sign_up_serializer = self.get_serializer(data=request.data)

        if sign_up_serializer.is_valid(raise_exception=True):

            user_object = sign_up_serializer.save()

            user_jwt_token = get_tokens_for_user(user_object)

            response_data = {
                **sign_up_serializer.data,
                "tokens": user_jwt_token
            }

            self.response_format["data"] = response_data
            self.response_format["message"] = messages.SIGNUP
            self.response_format["status_code"] = status.HTTP_201_CREATED

            return Response(self.response_format, status=self.response_format["status_code"])


class LoginUserAPIView(CreateAPIView):
    """
    Class for create an API for login user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginUserSerializer

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(LoginUserAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST method for login user and return auth token.
        """
        login_serializer = self.get_serializer(data=request.data)

        if login_serializer.is_valid(raise_exception=True):

            user_authenticated = authenticate(
                request,
                email=login_serializer.validated_data.get("email"),
                password=login_serializer.validated_data.get("password"))

            if user_authenticated:

                response_data = {
                    **UserDetailSerializer(user_authenticated).data,
                    "tokens": get_tokens_for_user(user_authenticated)
                }
                self.response_format["data"] = response_data
                self.response_format["message"] = messages.LOGIN
                self.response_format["status_code"] = status.HTTP_200_OK

            else:
                self.response_format["error"] = "invalid credentials"
                self.response_format["message"] = messages.INVALID_CRED
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST

            return Response(self.response_format, status=self.response_format["status_code"])


class ListUsersAPIView(ListAPIView):
    """
    Class for create user list api.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = UserDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter,)
    search_fields = ["=email", "name"]

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(ListUsersAPIView, self).__init__(**kwargs)

    def get_queryset(self):
        """
        Method for get user objects queryset.
        """
        return CustomUser.objects.exclude(id=self.request.user.id).order_by("id")

    def get(self, request, *args, **kwargs):
        """
        GET method for return the list of users in response.
        """
        list_users_serializer = super().list(request, *args, **kwargs)

        self.response_format["data"] = list_users_serializer.data
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = messages.FETCHED_SUCCESS.format("List of users are")

        return Response(self.response_format, status=self.response_format["status_code"])


class ListFriendUsersAPIView(ListAPIView):
    """
    Class for create friends user list api.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListFriendRequestSerializer
    pagination_class = CustomPagination

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(ListFriendUsersAPIView, self).__init__(**kwargs)

    def get_serializer_context(self):
        """
        Method for pass context to serializer class.
        """
        return {
            "user": self.request.user
        }

    def get_queryset(self):
        """
        Method for get user objects queryset.
        """
        user_id = self.request.user.id
        return FriendRequests.objects.select_related("requested_to").filter(
            Q(request_status="ACCEPTED"), Q(requested_by=user_id) | Q(requested_to=user_id)).order_by("id")

    def get(self, request, *args, **kwargs):
        """
        GET method for return the list of friend users in response.
        """
        list_friend_users_serializer = super().list(request, *args, **kwargs)

        self.response_format["data"] = list_friend_users_serializer.data
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = messages.FETCHED_SUCCESS.format("List of friend users are")

        return Response(self.response_format, status=self.response_format["status_code"])


class ListPendingFriendRequestAPIView(ListAPIView):
    """
    Class for creation pending a friend request list api.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListPendingFriendRequestSerializer
    pagination_class = CustomPagination

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(ListPendingFriendRequestAPIView, self).__init__(**kwargs)

    def get_queryset(self):
        """
        Method for get user objects queryset.
        """
        return FriendRequests.objects.select_related("requested_by").filter(
            requested_to=self.request.user.id, request_status="PENDING").distinct().order_by("id")

    def get(self, request, *args, **kwargs):
        """
        GET method for return the list of friend users in response.
        """
        list_friend_users_serializer = super().list(request, *args, **kwargs)

        self.response_format["data"] = list_friend_users_serializer.data
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = messages.FETCHED_SUCCESS.format("List of pending friend requests are")

        return Response(self.response_format, status=self.response_format["status_code"])


class FriendRequestActionAPIView(RetrieveAPIView):
    """
    Class for create friend request api.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = FriendRequestSerializer
    default_throttle_classes = [UserRateThrottle,]

    def __init__(self, **kwargs):
        """
        Constructor method for configuring response format.
        """
        self.response_format = ResponseInfo().response
        super(FriendRequestActionAPIView, self).__init__(**kwargs)

    def get_object(self):
        """
        Method for get friend request object.
        """
        return FriendRequests.objects.get(id=self.request.GET.get("request_id"))

    def check_object_permissions(self, request, obj):
        """
        Method for check permission on a friend request object.
        """
        if (obj.requested_to.id == request.user.id and
                (request.GET.get("request_action") == "ACCEPT" or request.GET.get("request_action") == "REJECT")):

            return True

        else:
            raise CustomException()

    def get_throttles(self):
        """
        Method for enable throttling based on condition.
        """
        if self.request.GET.get("request_action") == "SEND":
            return [throttle() for throttle in self.default_throttle_classes]

        return ()

    def get(self, request, *args, **kwargs):
        """
        GET method for return the list of friend users in response.
        """
        try:
            request_action = request.GET.get("request_action")
            if request_action == "SEND":
                requested_to = request.GET.get("requested_to")
                if requested_to is None:
                    raise CustomException(messages.REQUIRED.format("requested_to param"))

                data = {
                    "requested_by": request.user.id,
                    "requested_to": requested_to
                }

                friend_request_serializer = self.get_serializer(data=data)

                if friend_request_serializer.is_valid(raise_exception=True):
                    friend_request_serializer.save()

                    self.response_format["status_code"] = status.HTTP_201_CREATED
                    self.response_format["message"] = messages.FRIEND_REQUEST.format("send")

            else:
                if request.GET.get("request_id"):
                    if request_action == "ACCEPT":
                        friend_request_object = self.get_object()
                        self.check_object_permissions(request, friend_request_object)

                        if friend_request_object.request_status != "ACCEPTED":
                            friend_request_object.request_status = "ACCEPTED"
                            friend_request_object.save()

                            self.response_format["status_code"] = status.HTTP_200_OK
                            self.response_format["message"] = messages.FRIEND_REQUEST.format("accepted")
                        else:
                            self.response_format["status_code"] = status.HTTP_200_OK
                            self.response_format["message"] = messages.ALREADY_TOOK_ACTION.format("accepted")

                    elif request_action == "REJECT":
                        friend_request_object = self.get_object()
                        self.check_object_permissions(request, friend_request_object)

                        if friend_request_object.request_status != "REJECTED":
                            friend_request_object.request_status = "REJECTED"
                            friend_request_object.save()

                            self.response_format["status_code"] = status.HTTP_200_OK
                            self.response_format["message"] = messages.FRIEND_REQUEST.format("rejected")
                        else:
                            self.response_format["status_code"] = status.HTTP_200_OK
                            self.response_format["message"] = messages.ALREADY_TOOK_ACTION.format("rejected")

                    else:
                        self.response_format["error"] = "param required"
                        self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                        self.response_format["message"] = messages.REQUIRED.format("request_action param with (ACCEPT/SEND/REJECTED) is")

                else:
                    self.response_format["error"] = "id required"
                    self.response_format["status_code"] = status.HTTP_200_OK
                    self.response_format["message"] = messages.REQUIRED.format("request_id param")

        except FriendRequests.DoesNotExist:
            self.response_format["error"] = "friend request"
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = messages.DOES_NOT_EXIST.format("Friend request")

        return Response(self.response_format, status=self.response_format["status_code"])
