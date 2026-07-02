from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event, FoodItem
from .forms import EventForm, FoodItemForm

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@staff_member_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@staff_member_required
def event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})

@staff_member_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Food Item CRUD Views
@staff_member_required
def food_item_create(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save()
            return redirect('admin_dashboard')
    else:
        form = FoodItemForm()
    return render(request, 'events/food_item_form.html', {'form': form, 'title': 'Add Food Item'})

@staff_member_required
def food_item_update(request, item_id):
    food_item = get_object_or_404(FoodItem, pk=item_id)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            food_item = form.save()
            return redirect('admin_dashboard')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'events/food_item_form.html', {'form': form, 'title': 'Update Food Item'})

@staff_member_required
def food_item_delete(request, item_id):
    food_item = get_object_or_404(FoodItem, pk=item_id)
    if request.method == 'POST':
        food_item.delete()
        return redirect('admin_dashboard')
    return render(request, 'events/food_item_confirm_delete.html', {'food_item': food_item})
