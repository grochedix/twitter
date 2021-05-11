from django.urls import path, re_path

from .views import (AccountView, DetailTweetView, HomePageView, likeView,
                    redirect_homepage, retweetView, tweetView, commentView)

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("comment/<int:id>", commentView, name="comment"),
    path("tweet/", tweetView, name="tweet"),
    path("tweet/<int:pk>", DetailTweetView.as_view(), name="tweet-detail"),
    path("u/<str:username>", AccountView.as_view(), name="account-detail"),
    path("like/<int:id>", likeView, name="like"),
    path("retweet/<int:id>", retweetView, name="retweet"),
    path("", redirect_homepage),
]
