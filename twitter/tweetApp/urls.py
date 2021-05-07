from django.urls import path, re_path

from .views import HomePageView, redirect_homepage, tweetView

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("tweet/", tweetView, name="tweet"),
    path("", redirect_homepage),
]
