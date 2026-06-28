from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='avatars/', default='default_profile.jpg', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)