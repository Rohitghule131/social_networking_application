from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager
from utilities.mixins import CustomMixins
from utilities.messages import EMAIL_UNIQUE
from utilities.constant import REQUEST_STATUS


class CustomUser(AbstractBaseUser, CustomMixins):
    """
    Class for create user table.
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(
        _('email address'), unique=True, null=False, blank=False, error_messages={'unique': EMAIL_UNIQUE}
    )
    is_staff = models.BooleanField(null=False, blank=False, default=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_superuser = models.BooleanField(null=False, blank=False, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name",]

    objects = CustomUserManager()


class FriendRequests(CustomMixins):
    """
    Class for create friend request table.
    """
    requested_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name="request_user")
    requested_to = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name="request_friend")
    request_status = models.CharField(max_length=50, null=False, blank=False, choices=REQUEST_STATUS, default="PENDING")

    class Meta:
        unique_together = ('requested_by', 'requested_to',)
