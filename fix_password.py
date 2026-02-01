
import os
import django
import sys
from django.contrib.auth.models import User

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
django.setup()

# Nombre de usuario a modificar
USERNAME = 'leonardorevilla'
# Nueva contraseña temporal
NEW_PASSWORD = 'contraseña123'

try:
    # Buscar al usuario
    user = User.objects.get(username=USERNAME)
    # Establecer la nueva contraseña (esto la encripta)
    user.set_password(NEW_PASSWORD)
    # Guardar el cambio en la base de datos
    user.save()
    print(f"La contraseña para el usuario '{USERNAME}' ha sido restablecida correctamente.")
    print(f"Ahora puedes iniciar sesión con la contraseña temporal: {NEW_PASSWORD}")
    print("Por favor, cambia esta contraseña inmediatamente después de iniciar sesión.")

except User.DoesNotExist:
    print(f"Error: El usuario '{USERNAME}' no fue encontrado en la base de datos.")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")
