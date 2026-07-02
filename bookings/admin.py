from django.contrib import admin
from .models import Booking, Payment

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'event')
    search_fields = ('user__username', 'event__title')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'transaction_id', 'timestamp')
    list_filter = ('status',)

admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)
