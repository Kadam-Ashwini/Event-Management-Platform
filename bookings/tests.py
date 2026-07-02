from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from .models import Booking
from decimal import Decimal

class BookingCRUDTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a staff user
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        # Create an event
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date='2023-12-31',
            time='12:00:00',
            location='Test Location',
            price=Decimal('100.00')
        )
        # Create a booking
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            total_price=Decimal('100.00'),
            status='PENDING'
        )
        self.client = Client()

    def test_booking_edit_view_staff(self):
        self.client.login(username='staffuser', password='password')
        url = reverse('booking_edit', args=[self.booking.id])
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_edit.html')
        
        # Test POST (update status)
        response = self.client.post(url, {
            'status': 'CONFIRMED',
            'food_items': [] # Assuming no food items for simplicity
        })
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'CONFIRMED')

    def test_booking_delete_view_staff(self):
        self.client.login(username='staffuser', password='password')
        url = reverse('booking_delete', args=[self.booking.id])
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_confirm_delete.html')
        
        # Test POST (delete)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_booking_edit_view_non_staff(self):
        self.client.login(username='testuser', password='password')
        url = reverse('booking_edit', args=[self.booking.id])
        response = self.client.get(url)
        # Should redirect to login or show 302 because of @staff_member_required (which usually redirects to admin login)
        self.assertEqual(response.status_code, 302) 

    def test_booking_delete_view_non_staff(self):
        self.client.login(username='testuser', password='password')
        url = reverse('booking_delete', args=[self.booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
