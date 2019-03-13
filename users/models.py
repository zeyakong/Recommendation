from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from restaurant.models import Business


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass


class UserReview(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    stars = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
