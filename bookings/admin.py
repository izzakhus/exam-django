from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, Room, Booking


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description', 'image_tag')
    search_fields = ('name', 'location')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Image'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_number', 'hotel', 'price_per_night', 'capacity', 'is_available')
    list_filter = ('hotel', 'capacity')
    search_fields = ('number',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'check_in', 'check_out', 'total_price', 'status']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['user__username', 'room__room_number']
