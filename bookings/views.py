from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, BookingForm
from .models import Hotel, Room, Booking


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})


def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        # Здесь можно сделать запись в базу или что-то ещё
        print(f"Пользователь {request.user} забронировал отель: {hotel.name}")
        return redirect('hotel_list')  # возвращаемся на главную

    return redirect('hotel_list')


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
    return render(request, 'book_room.html', {'form': form, 'room': room})
