from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),  # Главная страница и список отелей
    path('book/<int:hotel_id>/', views.book_hotel, name='book_hotel'),  # Страница бронирования
]
