from django.contrib import admin

from .models import Comment, Follow, Like, Retweet, Tweet


@admin.register(Tweet, Retweet, Comment, Like, Follow)
class TweeterAdmin(admin.ModelAdmin):
    pass
