from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Booking
from .forms import BookingForm, PaymentForm, BookingEditForm
from events.models import Event

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            
            # Calculate total price
            food_items = form.cleaned_data['food_items']
            food_price = sum(item.price for item in food_items)
            booking.total_price = event.price + food_price
            
            booking.save()
            booking.food_items.set(food_items)
            
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'event': event})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Mock payment success
            from .models import Payment
            import uuid
            Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                transaction_id=f"TRANS_{uuid.uuid4()}",
                status='SUCCESS'
            )
            booking.status = 'CONFIRMED'
            booking.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    return render(request, 'bookings/payment.html', {'booking': booking, 'form': form})

@staff_member_required
def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            # Recalculate total price if food items changed
            food_items = form.cleaned_data['food_items']
            food_price = sum(item.price for item in food_items)
            booking.total_price = booking.event.price + food_price
            booking.save()
            booking.food_items.set(food_items)
            return redirect('admin_dashboard') # Redirect to admin dashboard
    else:
        form = BookingEditForm(instance=booking)
    return render(request, 'bookings/booking_edit.html', {'form': form, 'booking': booking})

@staff_member_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('admin_dashboard')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
