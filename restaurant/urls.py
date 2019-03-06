from django.urls import path

from . import views

app_name = 'restaurant'

urlpatterns = [
    path('search', views.search_result, name='search'),
    path('<str:business_id>', views.detail, name='detail'),
    path('<str:business_id>/review', views.add_review, name='add_review'),
    path('recommendation/<str:user_name>', views.generate_rec, name='generate_rec'),
]
