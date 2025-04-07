from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('book/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),

]
