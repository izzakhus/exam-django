from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Отель'
        verbose_name = 'Отель'

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Комнаты'
        verbose_name = 'Комнаты'

    def __str__(self):
        return f"Комната {self.room_number} — {self.hotel.name}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Booked')

    class Meta:
        verbose_name_plural = 'Бронирование'
        verbose_name = 'Бронирование'

    def __str__(self):
        return f"Бронь: {self.room.room_number} - {self.user.username} с {self.check_in} по {self.check_out}"

    def save(self, *args, **kwargs):
        nights = (self.check_out - self.check_in).days
        self.total_price = self.room.price_per_night * nights
        super(Booking, self).save(*args, **kwargs)
