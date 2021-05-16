from django.urls import path, re_path

from .views import loginView, logout_view, profileView, registerView

urlpatterns = [
    path("login/", loginView, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", registerView, name="register"),
    path("profile/", profileView, name="profile"),
]
