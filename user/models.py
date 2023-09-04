import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.manager import UserManager

"""
User choice selection fields below
"""

USER_PERMISSION_STATUS = (
    ("FPR", "FACULTY PRESIDENT"),
    ("DPR", "DEPARTMENT PRESIDENT"),
    ("GAD", "GENERAL ADMIN"),
)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        _("uid"), primary_key=True, default=uuid.uuid4, editable=False
    )

    # USER BASIC INFORMATION
    first_name = models.CharField(
        _("first name"), max_length=200, blank=False, null=False
    )
    middle_name = models.CharField(_("middle name"), max_length=200)
    last_name = models.CharField(
        _("last name"), max_length=200, blank=False, null=False
    )
    email = models.EmailField(
        _("email address"), max_length=200, blank=False, null=False, unique=True
    )
    phone_number = models.CharField(
        _("phone number"), max_length=15, blank=False, null=False, unique=True
    )
    password = models.CharField(_("password"), max_length=128, blank=False, null=False)

    # USER PERMISSION AND STATUS AND ROLE
    staff_role = models.CharField(
        _("user role"),
        max_length=100,
        choices=USER_PERMISSION_STATUS,
        blank=True,
        null=True,
    )
    is_admin = models.BooleanField(_("admin"), default=False)
    is_verified = models.BooleanField(_("verified"), default=False)
    is_active = models.BooleanField(_("active"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    # USER ACCOUNT LOGIN AND CREATION DATE
    last_login = models.DateTimeField(
        _("last login"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    created_at = models.DateTimeField(
        _("created date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    last_modified = models.DateTimeField(
        _("updated date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        # Deos the user has specific permission, yes!
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view app 'app_label'
        return True

    @property
    def is_staff(self):
        return self.is_admin
