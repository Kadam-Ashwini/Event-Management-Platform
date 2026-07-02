from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:event_id>/', views.submit_feedback, name='submit_feedback'),
]
