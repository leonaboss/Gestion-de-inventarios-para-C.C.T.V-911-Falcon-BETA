
import os
import django
import sys

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='leonardorevilla')
    print(f"User found: {user.username}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    # Check if a password is set (it will not be None or empty for a usable account)
    print(f"Password is set: {user.has_usable_password()}")
except User.DoesNotExist:
    print("User 'leonardorevilla' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
