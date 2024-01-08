import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # USER BASIC INFORMATION
    first_name = models.CharField(max_length=200, blank=False, null=False)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)

    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # USER ACCOUNT LOGIN AND CREATION DATE
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    last_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.first_name
