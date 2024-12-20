from rest_framework import serializers

from .models import (
    CustomUser,
    FriendRequests
)
from utilities.messages import (
    EMAIL_UNIQUE,
    VALID_PASSWORD
)
from chat.serializers import CreateChatConnectionSerializer


class SignUpUserSerializer(serializers.ModelSerializer):
    """
    Class for create serializer for serialize the data for sign up the user.
    """
    password = serializers.CharField(max_length=10, write_only=True)

    def validate(self, attrs):
        """
        Method for validate the signup data.
        """
        password = attrs.get("password")
        attrs["email"] = attrs["email"].lower()

        if not 5 <= len(password) <= 15:
            raise serializers.ValidationError(VALID_PASSWORD)

        try:
            CustomUser.objects.get(email=attrs["email"])
            raise serializers.ValidationError(EMAIL_UNIQUE)

        except CustomUser.DoesNotExist:
            pass

        return attrs

    def create(self, validated_data):
        """
        Create method used for create the user and return user object.
        """
        user = CustomUser.objects.create_user(
            name=validated_data.get("name"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )

        return user

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "password")


class LoginUserSerializer(serializers.Serializer):
    """
    Class for create serializer for serialize the data for sign up the user.
    """
    email = serializers.EmailField(allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=15, allow_null=False, allow_blank=False, write_only=True)

    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Class for create serializer for serialize the data for sign up the user.
    """
    class Meta:
        model = CustomUser
        fields = ("id", "email", "name")


class ListFriendRequestSerializer(serializers.ModelSerializer):
    """
    Class for serialize friend object.
    """
    friend = serializers.SerializerMethodField()

    def get_friend(self, obj):
        """
        Method for get user object and return user info dict.
        """
        if obj.request_status == "PENDING":
            return {
                "email": obj.requested_by.email,
                "name": obj.requested_by.name
            }
        if self.context.get("user").id == obj.requested_to.id:
            return {
                "email": obj.requested_by.email,
                "name": obj.requested_by.name
            }

        else:
            return {
                "email": obj.requested_to.email,
                "name": obj.requested_to.name
            }

    class Meta:
        model = FriendRequests
        fields = ("id", "friend")


class ListPendingFriendRequestSerializer(serializers.ModelSerializer):
    """
    Class for serialize friend object.
    """
    friend = serializers.SerializerMethodField()

    def get_friend(self, obj):
        """
        Method for get user object and return user info dict.
        """
        return {
            "email": obj.requested_by.email,
            "name": obj.requested_by.name
        }

    class Meta:
        model = FriendRequests
        fields = ("id", "friend")


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Class for serialize friend request.
    """

    class Meta:
        model = FriendRequests
        fields = ("id", "requested_to", "requested_by")


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Class for retreive user details.
    """

    class Meta:
        model = CustomUser
        fields = "__all__"
