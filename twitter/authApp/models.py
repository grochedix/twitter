from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    first_name = models.CharField(blank=False, null=False)
    last_name = models.CharField(blank=False, null=False)
    avatar = models.ImageField(upload_to="avatar/")
    city = models.CharField(blank=False, null=False)
    country = models.CharField(blank=False, null=False)
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
