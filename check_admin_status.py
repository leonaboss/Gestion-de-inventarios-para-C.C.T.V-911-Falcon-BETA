
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
django.setup()

from django.contrib.auth.models import User

def check_admin_status():
    """
    Encuentra al primer superusuario y muestra su estado.
    """
    try:
        # Busca cualquier superusuario. Si hay varios, el primero es suficiente para el diagnóstico.
        admin_user = User.objects.filter(is_superuser=True).first()

        if admin_user:
            print("--- Estado de la Cuenta de Superusuario ---")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"¿Está activa? (is_active): {admin_user.is_active}")
            print(f"¿Es staff? (is_staff): {admin_user.is_staff}")
            print(f"¿Es superusuario? (is_superuser): {admin_user.is_superuser}")
            print("-----------------------------------------")
            
            if not admin_user.is_active:
                print("\n[DIAGNÓSTICO]: La cuenta del superusuario está INACTIVA. Esta es la causa del problema de inicio de sesión.")
            elif not admin_user.is_staff:
                print("\n[DIAGNÓSTICO]: La cuenta del superusuario no es 'staff'. Esto podría impedir el acceso a ciertas áreas.")
            else:
                print("\n[DIAGNÓSTICO]: La cuenta parece estar configurada correctamente. Si el problema persiste, podría ser una contraseña incorrecta.")

        else:
            print("[ERROR]: No se encontró ninguna cuenta de superusuario en la base de datos.")

    except Exception as e:
        print(f"[ERROR]: Ocurrió un error al ejecutar el script: {e}")

if __name__ == "__main__":
    check_admin_status()
