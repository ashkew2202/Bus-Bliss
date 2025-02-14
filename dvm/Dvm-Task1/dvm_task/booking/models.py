from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class BusStops(models.Model):

    stop_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Bus Stops'
    
    def __str__(self):
        return self.stop_name

class BusServiceRegistration(models.Model):

    company = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Bus Registrations'
    
    def __str__(self):
        return self.company
    
class AddBus(models.Model):
    
    bus_name = models.CharField(max_length=100)
    seat_type = models.ManyToManyField(BusServiceRegistration, through = 'SeatInfo')
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Buses'

    def __str__(self):
        return self.bus_name
    
class Route(models.Model):
    bus_id = models.ForeignKey(AddBus, on_delete=models.CASCADE)
    stop_id = models.ManyToManyField(BusStops, through = 'BusStop')
    class Meta:
        verbose_name_plural = 'Routes'

class BusStop(models.Model):
    stop_id = models.ForeignKey(BusStops, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    class Meta:
        verbose_name_plural = 'Select Bus Stop'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    class Meta:
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return self.user.username

class SeatInfo(models.Model):
    
    bus_id = models.ForeignKey(AddBus, on_delete=models.CASCADE)
    bus_details = models.ForeignKey(BusServiceRegistration, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=100, choices=[('Luxury', 'Luxury'), ('Ordinary', 'Ordinary'), ('Sleeper', 'Sleeper')])
    seat_no = models.IntegerField()
    seat_price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    class Meta:
        verbose_name_plural = 'Seat Information'
    
    def __str__(self):
        return self.bus_id.bus_name + ' ' + self.seat_type + ' ' + str(self.seat_no)
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_id = models.ForeignKey(AddBus, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus_stop_id = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=100, choices=[('Luxury', 'Luxury'), ('Ordinary', 'Ordinary'), ('Sleeper', 'Sleeper')])
    class Meta:
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return self.user.username