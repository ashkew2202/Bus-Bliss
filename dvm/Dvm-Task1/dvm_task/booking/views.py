from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
from .models import Wallet, AddBus, BusStop, Route, SeatInfo

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
        seats = SeatInfo.objects.filter(bus_id=bus[0].id)
        user = User.objects.get(username=request.user.username)
        user_wallet = Wallet.objects.get_or_create(user=user)
        seats_requested = list()
        for seat in seats:
            print(request.POST.get(f'{seat.id}'))
            seats_requested.append(request.POST.get(f'{seat.id}'))
            if seat.seat_no < seats_requested[(seat.id-1)]:
                return render(request, 'infocollector.html', {'error': 'Not enough seats available'})
            elif seat.seat_no == seats_requested[(seat.id-1)]:
                seat.seat_no -= seats_requested[(seat.id-1)]
                seat.seat_availability = False
            else:
                seat.seat_no -= seats_requested[(seat.id-1)]
        balance = 0
        for i in range(len(seats_requested)):
            balance -= seats_requested[i] * seats[i].seat_price
        if user_wallet.balance + balance < 0:
            return redirect('/profile', {'error': 'Not enough balance, You only have ' + user_wallet.balance})
        else:
            user_wallet.balance += balance
            for seat in seats:
                seat.save()
            user_wallet.save()
    return render(request, 'infocollector.html')

def bookingconfirmotp(request):
    if request.method == 'POST':
        username = user.username
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
        return render(request, 'booking/confirmotp.html')