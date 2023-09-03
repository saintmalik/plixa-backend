from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

from .forms import RegisterUserChangeForm, RegisterUserCreationForm
from .models import CustomUsers




"""
==================================================================================================
    USER ADMINISTRATION SITE
==================================================================================================
"""
class CustomPlixaAdmin(admin.AdminSite):
    site_header = 'PLIXA ADMIN'
    site_title = 'PLIXA ADMINISTRATION'


custom_users = CustomPlixaAdmin(name='Plixa_Admin_Area')


"""
==================================================================================================
    CUSTOM USER ADMIN
==================================================================================================
"""
class CustomUserAdmin(UserAdmin):

    add_form = RegisterUserCreationForm
    form = RegisterUserChangeForm
    model = CustomUsers

    list_display = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'country', 'town_city', 'staff_role', 'is_admin', 'is_active', 'is_verified', 'last_login', 'created_date', 'updated_date',)

    list_filter = ('username', 'email', 'country', 'phone_number', 'staff_role', 'is_admin', 'is_active', 'is_verified', 'last_login', 'created_date', 'updated_date',)

    list_per_page = 5

    fieldsets = (
        (None, {
            "fields": ("first_name", "last_name", "username", "email","phone_number", "password",)}),

        ("Permissions", {
            "fields": ("is_admin", "is_active", "is_verified", "groups", "user_permissions")
        }),
    )

    add_fieldset = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name", "username", "email", "phone_number",
                 "password", "is_admin", "is_active", "is_verified", "groups", "user_permissions",
            )
        })
    )

    search_field = ("email", "username", "first_name", "last_name", "phone_number", "is_admin", "is_active", 'state', 'country', 'staff_role', 'last_login', 'created_date',)

    ordering = ("email", "username", "first_name", "last_name", "phone_number", "is_admin", "is_active", 'state', 'country', 'staff_role', 'last_login', 'created_date',)

    filter_horizontal = ()


# graphql_auth register
graphql_authen = apps.get_app_config('graphql_auth')

# refresh_token register
refresh_token = apps.get_app_config('refresh_token')

for model_name, model in graphql_authen.models.items() | refresh_token.models.items():
    custom_users.register(model)



# Register your admin here.
custom_users.register(CustomUsers, CustomUserAdmin)
