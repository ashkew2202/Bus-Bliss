from django.urls import path
from . import views as booking_views

urlpatterns = [
    path('',booking_views.home, name='booking-home'),
    path('profile/',booking_views.profile, name='booking-profile'),
    path('add_balance/',booking_views.user_add_balance, name='booking-add_balance'),
    path('verify_otp/',booking_views.verify_otp, name='booking-verify_otp'),
    path('send_otp/',booking_views.send_otp, name='booking-send_otp'),
    path('book/',booking_views.book, name='booking-book'),
    path('search-results/', booking_views.search, name='booking-results'),
    path('ticket/<int:route_id>/', booking_views.ticket, name='booking-ticket'),
    path('confirmbooking/<int:bus_id>/', booking_views.confirmbooking, name='booking-confirmbooking'),
    path('confirmotp/', booking_views.bookingconfirmotp, name='booking-confirmotp'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)