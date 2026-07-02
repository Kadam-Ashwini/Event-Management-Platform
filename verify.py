import os
import django
from django.test import Client
from django.utils import timezone
import datetime
import sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from events.models import Event, FoodItem
from bookings.models import Booking, Payment
from feedback.models import Feedback
from django.contrib.auth.models import User

def run_verification():
    print("Starting verification...")
    client = Client()

    # 1. Setup Data
    print("Setting up data...")
    # Create User
    user_password = 'password123'
    if User.objects.filter(username='testuser').exists():
        user = User.objects.get(username='testuser')
        user.set_password(user_password)
        user.save()
    else:
        user = User.objects.create_user(username='testuser', password=user_password, email='test@example.com')
    
    # Create Staff User
    staff_password = 'adminpassword'
    if User.objects.filter(username='adminuser').exists():
        staff = User.objects.get(username='adminuser')
        staff.set_password(staff_password)
        staff.is_staff = True
        staff.save()
    else:
        staff = User.objects.create_user(username='adminuser', password=staff_password, email='admin@example.com', is_staff=True)

    # Create Food Items
    burger = FoodItem.objects.create(name='Burger', price=10.00)
    salad = FoodItem.objects.create(name='Salad', price=8.00, is_vegetarian=True)

    # Create Event
    event = Event.objects.create(
        title='Tech Conference 2025',
        description='A great tech conference.',
        date=timezone.now().date() + datetime.timedelta(days=10),
        time=datetime.time(10, 0),
        location='Convention Center',
        price=100.00
    )

    # 2. Test Registration (Skipping as we created user manually, but testing login)
    print("Testing Login...")
    login_response = client.post('/accounts/login/', {'username': 'testuser', 'password': user_password})
    if login_response.status_code == 302:
        print("Login Successful")
    else:
        print(f"Login Failed: {login_response.status_code}")

    # 3. Test Event Listing
    print("Testing Event Listing...")
    response = client.get('/')
    if event.title in str(response.content):
        print("Event listed successfully")
    else:
        print("Event not found in list")

    # 4. Test Booking
    print("Testing Booking...")
    # Select food items
    response = client.post(f'/bookings/book/{event.id}/', {'food_items': [burger.id, salad.id]})
    if response.status_code == 302:
        print("Booking created, redirected to payment")
        booking = Booking.objects.get(user=user, event=event)
        print(f"Booking ID: {booking.id}, Total Price: {booking.total_price}")
        
        # 5. Test Payment
        print("Testing Payment...")
        payment_url = response.url
        # Post to payment page with card details
        response = client.post(payment_url, {
            'card_number': '1234567812345678',
            'expiry_date': '12/25',
            'cvv': '123'
        })
        if response.status_code == 302:
            print("Payment successful, redirected to success page")
            booking.refresh_from_db()
            if booking.status == 'CONFIRMED':
                print("Booking confirmed")
            else:
                print(f"Booking status: {booking.status}")
        else:
            print(f"Payment failed: {response.status_code}")
    else:
        print(f"Booking failed: {response.status_code}")

    # 6. Test Feedback
    print("Testing Feedback...")
    response = client.post(f'/feedback/submit/{event.id}/', {'rating': 5, 'comment': 'Great event!'})
    if response.status_code == 302:
        print("Feedback submitted successfully")
        if Feedback.objects.filter(user=user, event=event).exists():
            print("Feedback exists in DB")
    else:
        print(f"Feedback failed: {response.status_code}")

    # 7. Test Admin Dashboard
    print("Testing Admin Dashboard...")
    client.logout()
    client.login(username='adminuser', password=staff_password)
    response = client.get('/reports/dashboard/')
    if response.status_code == 200:
        print("Dashboard accessed successfully")
        if str(booking.total_price) in str(response.content): # Check if revenue is shown (simple check)
            print("Revenue data found in dashboard")
        if 'Add New Event' in str(response.content):
            print("Add Event button found")
        if 'Manage Users' in str(response.content):
            print("Manage Users button found")
    else:
        print(f"Dashboard access failed: {response.status_code}")

    # Cleanup
    print("Cleaning up...")
    user.delete()
    staff.delete()
    event.delete()
    burger.delete()
    salad.delete()
    print("Verification Complete.")

if __name__ == '__main__':
    run_verification()
