from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
from .models import Wallet, AddBus, BusStop, Route, SeatInfo, Booking

def home(request):
    return render(request, 'booking/home.html')

def profile(request):
    username = request.user.username
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    context = {
        'balance':wallet.balance,
    }
    return render(request, 'account/profile.html', context=context)

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session['otp']:
            user = User.objects.get(username=request.session['username'])
            user.is_verified = True
            user.save()
            return redirect('account_login')
        else:
            return render(request, 'account/getotp.html', {'error': 'Invalid OTP'})
    return render(request, 'account/getotp.html')

def user_add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount == '' or float(amount) < 0:
            return render(request, 'account/add_balance.html', {'error': 'Please enter a valid amount'})
        username = request.user.username
        user = User.objects.get(username=username)
        wallet, created = Wallet.objects.get_or_create(user=user)
        wallet.balance += float(amount)
        wallet.save()
        return redirect('/profile')
    return render(request, 'account/add_balance.html')

def send_otp(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST.get('username')
        user, created = User.objects.get_or_create(username=username, email=request.POST.get('email'), password=request.POST.get('password')) 
        print(user)
        otp = random.randint(100000, 999999)
        request.session['otp'] = str(otp)
        request.session['username'] = username
        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return redirect('/verify_otp')
    return render(request, 'account/getotp.html')

def book(request):
    return render(request, 'booking/book.html')

def search(request):
    if request.method == 'GET':
        from_place = request.GET['from']
        to_place = request.GET['to']
        date = request.GET['date']
        routes = list()
        stops = BusStop.objects.filter(date=date).order_by('arrival_time')
        for stop in stops:
            if stop.stop_id.stop_name == from_place:
                routes.append(Route.objects.filter(id=stop.route_id_id))
                
        if routes is None:
            return render(request, 'booking/results.html', {'error': 'No buses available'})
        
        options = list()
        print(routes)
        for route in routes:
            bus = AddBus.objects.filter(id=route[0].bus_id_id)
            stops = BusStop.objects.filter(route_id = route[0].id)
            for stop in stops:
                if stop.stop_id.stop_name == from_place:
                    from_arrival_time = stop.arrival_time
                    from_departure_time = stop.departure_time
                if stop.stop_id.stop_name == to_place:
                    to_arrival_time = stop.arrival_time
            if from_arrival_time > to_arrival_time:
                continue
            options.append({
                'route_id': route[0].id,
                'bus_name': bus[0],
                'from_arrival_time': from_arrival_time,
                'from_departure_time': from_departure_time,
                'to_arrival_time': to_arrival_time,
                'initial_price': SeatInfo.objects.filter(bus_id=bus[0].id)[0].seat_price
            })

        context = {
            'options': options
        }
    return render(request, 'booking/results.html', context)

def ticket(request, route_id):
    bus = AddBus.objects.filter(id=Route.objects.filter(id=route_id)[0].bus_id_id)[0]
    seats = SeatInfo.objects.filter(bus_id=bus.id)
    context = {
        'bus': bus,
        'seats': seats
    }
    return render(request, 'booking/ticket.html', context)

def confirmbooking(request, bus_id):
    if request.method=='POST':
        bus = AddBus.objects.filter(id=bus_id)
        seats = SeatInfo.objects.filter(bus_id=bus_id)
        user = User.objects.get(username=request.user.username)
        seats_requested = dict()
        seats_requested1 = list()
        for seat in seats:
            seat_type = seat.seat_type
            requested_seat_count = int(request.POST.get(f'{seat.id}'))
            seats_requested[seat_type] = requested_seat_count
            seats_requested1.append((seat_type, requested_seat_count, seat.seat_price))
        price = 0
        for seat_type, count, seat_price in seats_requested1:
            price += count * seat_price
        booking = Booking.objects.create(user=user, bus_id = bus[0], totalPrice=price, seats_requested=seats_requested)
        booking.save()
        return redirect('/confirmotp')
    return render(request, 'infocollector.html')

def verifybooking(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session['otp']:
            user = User.objects.get(username=request.session['username'])
            booking = Booking.objects.get(user=user)
            booking.is_verified = True
            booking.save()
            return redirect('account_login')
        else:
            return render(request, 'booking/confirmotp.html', {'error': 'Invalid OTP'})
    return render(request, 'account/confirmotp.html')

def bookingconfirmotp(request):
    print(request.method)
    if request.method == 'GET':
        username = user
        user, created = User.objects.get(username=username) 
        print(user)
        otp = random.randint(100000, 999999)
        request.session['otp'] = str(otp)
        request.session['username'] = username
        send_mail(
            'OTP Verification For Booking',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return redirect('/verifybooking')
    return render(request, 'account/confirmotp.html')