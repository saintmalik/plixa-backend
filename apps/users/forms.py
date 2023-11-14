from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
)
from django.forms import ModelForm

from .models import User


class RegisterUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
        )

        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "middle_name": forms.TextInput(),
            "email": forms.EmailInput(),
            "phone_number": forms.NumberInput(),
        }

        labels = {
            "first_name": "first name",
            "last_name": "last name",
            "middle_name": "middle name",
            "email": "email address",
            "phone_number": "phone number",
        }

    def clean_register_data(self):
        data = self.cleaned_data[
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
        ]

        return data


class LoginProfile(ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")

        widgets = {
            "email": forms.EmailInput(),
            "password": forms.PasswordInput(),
        }

        labels = {
            "email": "email",
            "password": "password",
        }

    def clean_register_data(self):
        data = self.cleaned_data["email", "password"]

        return data


class RegisterUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "phone_number",
            "email",
        )

        label = {
            "phone_number": "phone number",
            "email": "email",
        }

        widget = {
            "phone_number": forms.NumberInput(),
            "email": forms.EmailInput(),
        }
