from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Rating

admin.site.register(User)

admin.site.register(Rating)
