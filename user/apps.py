from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"


class UserAdminConfig(AdminConfig):
    default_site = "user.admin.PlixaAdmin"
