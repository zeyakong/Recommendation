from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class UserReview(models.Model):
    rating_id = models.CharField(primary_key=True,max_length=200)
    user_name = models.CharField(max_length=200)
    business_id = models.CharField(max_length=200)
    stars = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
