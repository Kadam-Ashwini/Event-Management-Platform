from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('edit/<int:booking_id>/', views.booking_edit, name='booking_edit'),
    path('delete/<int:booking_id>/', views.booking_delete, name='booking_delete'),
]
