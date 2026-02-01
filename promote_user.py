import os
import django
import argparse
import sys

# Add project root to Python path
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error during Django setup: {e}")
    sys.exit(1)

from django.contrib.auth.models import User

def promote_user(username):
    """
    Finds a user by username and grants them staff and superuser permissions.
    """
    try:
        user = User.objects.get(username__iexact=username)
        
        updated = False
        if not user.is_staff:
            user.is_staff = True
            updated = True
            print(f"✅ Permiso de 'staff' otorgado a '{user.username}'.")
            
        if not user.is_superuser:
            user.is_superuser = True
            updated = True
            print(f"✅ Permiso de 'superuser' otorgado a '{user.username}'.")

        if updated:
            user.save()
            print(f"🚀 ¡Éxito! El usuario '{user.username}' ahora es administrador.")
        else:
            print(f"ℹ️ El usuario '{user.username}' ya es un administrador.")

    except User.DoesNotExist:
        print(f"❌ Error: No se encontró un usuario con el nombre '{username}'.")
    except Exception as e:
        print(f"🚨 Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Promocionar un usuario a administrador (staff y superuser).",
        epilog="Ejemplo de uso: python promote_user.py leonardorevilla"
    )
    parser.add_argument(
        "username", 
        type=str, 
        help="El nombre de usuario exacto de la cuenta a promocionar."
    )
    
    args = parser.parse_args()
    
    promote_user(args.username)