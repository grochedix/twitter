from django.contrib.auth import get_user_model
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=280, blank=True, null=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="tweets"
    )
    image = models.ImageField(upload_to="tweets/%Y/%m/%d/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Tweet {self.id} by {self.author.username}"


class Retweet(models.Model):
    tweet = models.ForeignKey(
        to=Tweet, on_delete=models.CASCADE, related_name="retweets"
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="retweets"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Retweet {self.id} by {self.author.username} of tweet {self.tweet.id}"


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment {self.id} by {self.author.username} of tweet {self.tweet.id}"


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="likes"
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["tweet", "user"]


class Follow(models.Model):
    followed = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="followers"
    )
    follower = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="follows"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed} is followed by {self.follower}"
