from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from decimal import Decimal

class EventCRUDTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.client = Client()

    def test_event_create_view(self):
        self.client.login(username='staffuser', password='password')
        url = reverse('event_create')
        response = self.client.post(url, {
            'title': 'New Event',
            'description': 'New Description',
            'date': '2024-01-01',
            'time': '10:00:00',
            'location': 'New Location',
            'price': '50.00'
        })
        self.assertEqual(response.status_code, 302) # Redirects to detail
        self.assertTrue(Event.objects.filter(title='New Event').exists())

    def test_event_update_view(self):
        event = Event.objects.create(
            title='Old Event',
            description='Old Description',
            date='2024-01-01',
            time='10:00:00',
            location='Old Location',
            price=Decimal('50.00')
        )
        self.client.login(username='staffuser', password='password')
        url = reverse('event_update', args=[event.id])
        response = self.client.post(url, {
            'title': 'Updated Event',
            'description': 'Updated Description',
            'date': '2024-01-01',
            'time': '10:00:00',
            'location': 'Updated Location',
            'price': '60.00'
        })
        self.assertEqual(response.status_code, 302)
        event.refresh_from_db()
        self.assertEqual(event.title, 'Updated Event')
        self.assertEqual(event.price, Decimal('60.00'))

    def test_event_delete_view(self):
        event = Event.objects.create(
            title='Delete Me',
            description='Description',
            date='2024-01-01',
            time='10:00:00',
            location='Location',
            price=Decimal('50.00')
        )
        self.client.login(username='staffuser', password='password')
        url = reverse('event_delete', args=[event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(title='Delete Me').exists())
