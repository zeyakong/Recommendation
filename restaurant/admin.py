from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Business, Review, Customer


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stars', 'review_count')


admin.site.register(Business, BusinessAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'business_id', 'text', 'stars')


admin.site.register(Review, ReviewAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'average_stars')


admin.site.register(Customer, CustomerAdmin)

