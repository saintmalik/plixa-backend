from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.forms import RegisterUserChangeForm, RegisterUserCreationForm
from user.models import User


class PlixaAdmin(admin.AdminSite):
    site_header = "PLIXA ADMIN"
    site_title = "PLIXA ADMINISTRATION"


user_admin = PlixaAdmin(name="Plixa_Admin_Area")


class UserAdmin(BaseUserAdmin):
    add_form = RegisterUserCreationForm
    form = RegisterUserChangeForm
    model = User

    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "staff_role",
        "is_admin",
        "is_active",
        "is_verified",
        "last_login",
        "created_at",
        "last_modified",
    )

    list_filter = (
        "email",
        "phone_number",
        "staff_role",
        "is_admin",
        "is_active",
        "is_verified",
        "last_login",
        "created_at",
        "last_modified",
    )

    list_per_page = 5

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldset = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "password",
                "is_admin",
                "is_active",
                "is_verified",
                "groups",
                "user_permissions",
            ),
        },
    )

    search_field = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_admin",
        "is_active",
        "staff_role",
        "last_login",
        "created_at",
    )

    ordering = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_admin",
        "is_active",
        "staff_role",
        "last_login",
        "created_at",
    )

    filter_horizontal = ()


# graphql_auth register
graphql_authen = apps.get_app_config("graphql_auth")

# refresh_token register
refresh_token = apps.get_app_config("refresh_token")

for model_name, model in graphql_authen.models.items() | refresh_token.models.items():
    user_admin.register(model)


# Register your admin here.
user_admin.register(User, UserAdmin)
