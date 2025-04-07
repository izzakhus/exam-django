from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, BookingForm
from .models import Hotel, Room, Booking


def hotel_list(request):
    hotels = Hotel.objects.all()

    context = {'hotels': hotels}
    return render(request, 'hotel_list.html', context)


def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = hotel.rooms.first()

    if request.method == 'POST':
        print(f"Пользователь {request.user} забронировал отель: {hotel.name}")
        return redirect('hotel_list')

    context = {'hotel': hotel, 'room': room}
    return render(request, 'book_hotel.html', context)


def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.total_price = room.price_per_night * (
                    form.cleaned_data['check_out'] - form.cleaned_data['check_in']).days
            booking.save()
            return redirect('hotel_list')
    else:
        form = BookingForm(initial={'room': room})

    context = {'form': form, 'room': room}
    return render(request, 'book_room.html', context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = hotel.room_set.first()

    context = {'room': room}
    return render(request, 'hotel_detail.html', context)
