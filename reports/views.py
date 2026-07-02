from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from bookings.models import Booking, Payment
from events.models import Event, FoodItem

@staff_member_required
def admin_dashboard(request):
    total_bookings = Booking.objects.count()
    total_revenue = Payment.objects.filter(status='SUCCESS').aggregate(Sum('amount'))['amount__sum'] or 0
    total_events = Event.objects.count()
    
    # Recent bookings
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    # Recent events
    recent_events = Event.objects.order_by('date')[:10]
    
    # Food items
    food_items = FoodItem.objects.all()
    
    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_events': total_events,
        'recent_bookings': recent_bookings,
        'recent_events': recent_events,
        'food_items': food_items,
    }
    return render(request, 'reports/admin_dashboard.html', context)
