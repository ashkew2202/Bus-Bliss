from django.contrib import admin
from django.contrib.auth.models import User
from .models import BusStops, AddBus, Route, Wallet, BusStop, BusServiceRegistration, SeatInfo, Booking

class Administration (admin.AdminSite):
    site_header = 'Booking Administration'

adminSite= Administration(name='admin')

class MyInline(admin.TabularInline):
    model = BusStop
    extra = 1

class BusDetailsInline(admin.TabularInline):
    model = SeatInfo
    extra = 1

class BusStopAdmin(admin.ModelAdmin):
    inlines = [MyInline]

class BusAdmin(admin.ModelAdmin):
    inlines = [BusDetailsInline]
    
adminSite.register(BusStops)
adminSite.register(AddBus, BusAdmin)
adminSite.register(Route, BusStopAdmin)
adminSite.register(Wallet)
adminSite.register(BusServiceRegistration)
adminSite.register(User)
adminSite.register(Booking)