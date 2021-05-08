from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    avatar = models.ImageField(upload_to="avatar/", default="avatar/default.png")
    background = models.ImageField(upload_to="background/", default="background/default_background.png")
    city = models.CharField(blank=False, null=False, max_length=100)
    country = models.CharField(blank=False, null=False, max_length=100)
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
