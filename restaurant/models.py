from django.db import models


# Create your models here.
class Business(models.Model):
    business_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    stars = models.CharField(max_length=20)
    review_count = models.CharField(max_length=20)
    is_open = models.CharField(max_length=20)
    attributes = models.CharField(max_length=500)
    categories = models.CharField(max_length=200)
    hours = models.CharField(max_length=200)
    #
    # class Meta:
    #     abstract = True
    #     ordering = ['-starts']


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=200)
    user_id = models.CharField(max_length=200)
    business_id = models.CharField(max_length=200)
    stars = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    useful = models.CharField(max_length=20)
    funny = models.CharField(max_length=20)
    cool = models.CharField(max_length=20)


class Customer(models.Model):
    user_id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=20)
    average_stars = models.CharField(max_length=20)
