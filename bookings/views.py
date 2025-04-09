from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, BookingForm
from .models import Hotel, Room, Booking
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date


def hotel_list(request):
    hotels = Hotel.objects.all()

    context = {'hotels': hotels}
    return render(request, 'hotel_list.html', context)



@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = hotel.rooms.first()

    if request.method == 'POST':
        check_in = parse_date(request.POST['check_in'])
        check_out = parse_date(request.POST['check_out'])

        if check_in and check_out:
            nights = (check_out - check_in).days

            booking = Booking(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                total_price=room.price_per_night * nights,
            )
            booking.save()

            return redirect('booking_confirmation')

    return render(request, 'book_hotel.html', {'hotel': hotel, 'room': room})


def booking_confirmation(request):
    booking = Booking.objects.last()
    hotel = booking.room.hotel
    room = booking.room

    return render(request, 'book_confirmation.html', {
        'booking': booking,
        'hotel': hotel,
        'room': room,
    })


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