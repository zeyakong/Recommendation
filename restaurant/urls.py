from django.urls import path

from . import views

appName = 'restaurant'
urlpatterns = [
    path('search/', views.search_result, name='search_result'),
    path('<str:business_id>/', views.detail, name='detail'),
]
