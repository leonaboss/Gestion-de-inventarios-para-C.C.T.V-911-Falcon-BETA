
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
django.setup()

from django.contrib.auth.models import User

def reactivate_admin():
    """
    Busca al primer superusuario y se asegura de que su cuenta esté activa y sea staff.
    Este script es una medida correctiva para restaurar el acceso.
    """
    try:
        # Busca cualquier superusuario.
        admin_user = User.objects.filter(is_superuser=True).first()

        if admin_user:
            print(f"--- Reactivando la cuenta de: {admin_user.username} ---")
            
            changes_made = False
            if not admin_user.is_active:
                admin_user.is_active = True
                print("[CORRECCIÓN]: La cuenta ha sido reactivada (is_active = True).")
                changes_made = True
            
            if not admin_user.is_staff:
                admin_user.is_staff = True
                print("[CORRECCIÓN]: Se ha restaurado el permiso de staff (is_staff = True).")
                changes_made = True

            if changes_made:
                admin_user.save()
                print("\n¡Éxito! La cuenta del superusuario ha sido actualizada.")
                print("Por favor, intenta iniciar sesión de nuevo.")
            else:
                print("\nLa cuenta ya estaba activa y configurada como staff. No se necesitaron cambios.")
                print("Si aún no puedes iniciar sesión, el problema puede ser la contraseña.")

            print("-------------------------------------------------")

        else:
            print("[ERROR]: No se encontró ninguna cuenta de superusuario en la base de datos.")

    except Exception as e:
        print(f"[ERROR]: Ocurrió un error al ejecutar el script de reactivación: {e}")

if __name__ == "__main__":
    reactivate_admin()
