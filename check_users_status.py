
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
django.setup()

from django.contrib.auth.models import User

def check_users():
    """
    Lista todos los usuarios en el sistema y muestra su estado.
    """
    print("--- Estado de Usuarios ---")
    users = User.objects.all().order_by('id')
    if not users:
        print("No se encontraron usuarios en la base de datos.")
        return

    for user in users:
        estado = []
        if user.is_active:
            estado.append("Activo")
        else:
            estado.append("Inactivo")
        
        if user.is_staff:
            estado.append("Staff")

        if user.is_superuser:
            estado.append("Superuser")
            
        print(f"ID: {user.id}, Username: '{user.username}', Estado: {', '.join(estado)}")
    
    print("--------------------------")

if __name__ == "__main__":
    check_users()
