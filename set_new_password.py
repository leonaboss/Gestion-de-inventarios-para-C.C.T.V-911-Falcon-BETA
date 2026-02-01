import os
import django
import argparse

# Es importante configurar el entorno de Django ANTES de importar los modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_inv.settings')
django.setup()

from django.contrib.auth.models import User

def set_new_password(username, password):
    """
    Busca un usuario por su nombre de usuario. Si existe, establece su nueva contraseña 
    y se asegura de que sea un superusuario activo. Si no existe, crea un nuevo 
    superusuario con esa contraseña.
    """
    try:
        user = User.objects.get(username=username)
        print(f"Usuario '{username}' encontrado. Actualizando contraseña y permisos...")
        
        # Establece la nueva contraseña encriptada
        user.set_password(password)
        
        # Se asegura de que el usuario tenga todos los permisos de administrador
        if not user.is_superuser:
            user.is_superuser = True
            print(f" -> Promovido a superusuario.")
        
        if not user.is_staff:
            user.is_staff = True
            print(f" -> Permisos de 'staff' otorgados.")

        if not user.is_active:
            user.is_active = True
            print(f" -> Cuenta activada.")

        user.save()
        print(f"\n¡Éxito! La contraseña para '{username}' ha sido cambiada y tiene todos los privilegios de administrador.")

    except User.DoesNotExist:
        print(f"Usuario '{username}' no encontrado. Creando un nuevo superusuario...")
        User.objects.create_superuser(username, '', password)
        print(f"\n¡Éxito! Superusuario '{username}' creado con la contraseña especificada.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cambia la contraseña de un usuario de Django y/o lo convierte en superusuario.",
        epilog="Ejemplo de uso: python set_new_password.py tu_admin nueva_clave_segura"
    )
    parser.add_argument('username', type=str, help='El nombre de usuario del administrador.')
    parser.add_argument('password', type=str, help='La nueva contraseña que deseas establecer.')

    args = parser.parse_args()
    
    set_new_password(args.username, args.password)
