from django.contrib.auth import get_user_model
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=280)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tweets/%Y/%m/%d/")
    date = models.DateTimeField(auto_now_add=True)


class Retweet(Tweet):
    tweet = models.ForeignKey(
        to=Tweet, on_delete=models.CASCADE, related_name="retweets"
    )
