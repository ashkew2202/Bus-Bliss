from django.urls import path
from . import views as booking_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path(
        '',
        booking_views.home,
        name='booking-home'),
    path(
        'profile/',
        booking_views.profile,
        name='booking-profile'),
    path(
        'add_balance/',
        booking_views.user_add_balance,
        name='booking-add_balance'),
    path(
        'verify_otp/',
        booking_views.verify_otp,
        name='booking-verify_otp'),
    path(
        'send_otp/',
        booking_views.send_otp,
        name='booking-send_otp'),
    path(
        'book/',
        booking_views.book,
        name='booking-book'),
    path(
        'search-results/',
        booking_views.search,
        name='booking-results'),
    path(
        'ticket/<int:route_id>/',
        booking_views.ticket,
        name='booking-ticket'),
    path(
        'confirmbooking/<int:bus_id>/',
        booking_views.confirmbooking,
        name='booking-confirmbooking'),
    path(
        'confirmotp/',
        booking_views.bookingconfirmotp,
        name='booking-confirmotp'),
    path(
        'verifybooking/',
        booking_views.verifybooking,
        name='booking-verifybooking'),
    path(
        'ticketinfo/',
        booking_views.showticketinfo,
        name='booking-ticketinfo'),
    path(
        'cancelbooking/',
        booking_views.cancelBooking,
        name='booking-cancelbooking'),
    path(
        'search-autocomplete/',
        booking_views.searchAutoComplete,
        name='booking-search-autocomplete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
