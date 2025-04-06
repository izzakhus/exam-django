from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hotel_list, name='home'),
    path('register/', views.register, name='register'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('book/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
]
