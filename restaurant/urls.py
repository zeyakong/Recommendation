from django.urls import path

from . import views

app_name = 'restaurant'

urlpatterns = [
    path('search/', views.search_result, name='search'),
    path('<str:business_id>/', views.detail, name='detail'),
]
