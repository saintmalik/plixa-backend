from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self, email: str, first_name: str, last_name: str, password: str, **extra_fields
    ):
        if not email:
            raise ValueError(
                "email address not provided. please provide an email address"
            )
        if not first_name:
            raise ValueError("first name not provided. please provide a first name")
        if not last_name:
            raise ValueError("last name not provided. please provide a last name")

        email = self.normalize_email(email)

        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self, email: str, first_name: str, last_name: str, password: str, **extra_fields
    ):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("user must have is_admin set to True to be a superuser")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "user must have is_superuser set to True to be a superuser"
            )

        return self.create_user(email, first_name, last_name, password, **extra_fields)
