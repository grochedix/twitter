from django.urls import path, re_path

from .views import HomePageView, redirect_homepage, tweetView, AccountView

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("tweet/", tweetView, name="tweet"),
    path("u/<str:username>", AccountView.as_view(), name="account-detail"),
    path("", redirect_homepage),
]
