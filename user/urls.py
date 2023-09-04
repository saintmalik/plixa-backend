from django.urls import path

from .views import HomeView


app_name = "users"


urlpatterns = [
    path("", HomeView.as_view(), name="users"),
]
