from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm
from events.models import Event

@login_required
def submit_feedback(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.event = event
            feedback.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form, 'event': event})
