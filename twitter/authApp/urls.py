from django.urls import path, re_path
from .views import loginView, registerView, logout_view, profileView

urlpatterns = [
    path("login/", loginView, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", registerView, name="register"),
    path("profile/", profileView, name="profile"),
]
