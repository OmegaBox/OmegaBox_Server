from django.contrib import admin

from reservations.models import Reservation, Payment


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
