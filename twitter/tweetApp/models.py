from django.contrib.auth import get_user_model
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=280)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tweets/%Y/%m/%d/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


class Retweet(Tweet):
    tweet = models.ForeignKey(
        to=Tweet, on_delete=models.CASCADE, related_name="retweets"
    )


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=280)
    image = models.ImageField(upload_to="tweets/%Y/%m/%d/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="likes"
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    followed = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="followers"
    )
    follower = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="follows"
    )
    date = models.DateTimeField(auto_now_add=True)
