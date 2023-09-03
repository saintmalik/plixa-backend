from datetime import datetime

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    """
    custom user model is extended from BaseUserManager to modified the default user manager
    """

    def create_user(self, email, first_name, last_name, username, phone_number, password, **extra_fields):
        
        if not first_name:
            raise ValueError(_("first name must be provided"))
        if not last_name:
            raise ValueError(_("last name must be provided"))
        if not username:
            raise ValueError(_("username must be provided"))
        if not phone_number:
            raise ValueError(_('user must provide phone number'))
        if not email:
            raise ValueError(_("users must have email address"))
        
        email = self.normalize_email(email)
        created_date = str(datetime.now())
        
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            username = username,
            phone_number = phone_number,
            created_date=created_date,
            **extra_fields
            )
        
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email, first_name, last_name, username, phone_number, password, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_("user must have is_admin=True."))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('user must have is_superuser=True.'))
        
        return self.create_user(email, first_name, last_name, username, phone_number, password, **extra_fields)

