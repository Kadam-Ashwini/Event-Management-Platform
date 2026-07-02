import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'adminpassword'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists.")
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"Password for '{username}' updated to '{password}'.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
