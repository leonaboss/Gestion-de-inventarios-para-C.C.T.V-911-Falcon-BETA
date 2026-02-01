import os
import django
import argparse
import sys

# It's crucial to add the project's root directory to the Python path
# to ensure that modules like 'sistema_inv' can be found.
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error during Django setup: {e}")
    print("\nPlease ensure you are running this script from the root directory of your Django project.")
    sys.exit(1)

from django.contrib.auth.models import User

def reactivate_user(username):
    """
    Finds a user by their username and sets their is_active flag to True.
    """
    try:
        user = User.objects.get(username__iexact=username) # Case-insensitive lookup
        if user.is_active:
            print(f"✅ El usuario '{user.username}' ya se encuentra activo.")
        else:
            user.is_active = True
            user.save()
            print(f"🚀 ¡Éxito! El usuario '{user.username}' ha sido reactivado.")
    except User.DoesNotExist:
        print(f"❌ Error: No se encontró un usuario con el nombre '{username}'. Verifica que el nombre sea correcto.")
    except Exception as e:
        print(f"🚨 Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reactivar una cuenta de usuario de Django marcándola como 'activa'.",
        epilog="Ejemplo de uso: python reactivate_user.py tu_admin"
    )
    parser.add_argument(
        "username", 
        type=str, 
        help="El nombre de usuario exacto de la cuenta a reactivar."
    )
    
    args = parser.parse_args()
    
    reactivate_user(args.username)
