from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate, login
from .forms import UsuarioForm, PublicUsuarioForm
from .models import Perfil
from django.contrib import messages


def crear_usuario_publico(request):
    """
    Permite a cualquier usuario crear una cuenta nueva.
    """
    if request.method == 'POST':
        form = PublicUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # El método save del formulario ahora maneja toda la lógica.
            messages.success(request, '¡Cuenta creada con éxito! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = PublicUsuarioForm()
    return render(request, 'login3.html', {'form': form})


# Solo el admin puede gestionar usuarios
def es_admin(user):
    return user.is_staff

@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        # Pass the request user to the form for validation logic
        form = UsuarioForm(request.POST, user=request.user)
        if form.is_valid():
            form.save() # The form's save method handles everything
            
            # The username is available after form validation
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuario '{username}' creado correctamente.")
            return redirect('admin_panel')
    else:
        form = UsuarioForm(user=request.user)

    return render(request, 'form_usuarios.html', {'form': form})

@user_passes_test(es_admin)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Pass the request user to the form for validation logic
        form = UsuarioForm(request.POST, instance=usuario, user=request.user)
        if form.is_valid():
            # The form's save method now contains all the logic
            # for correctly handling the password and security phrase.
            form.save()

            # Handle session update for admin self-editing password
            password = form.cleaned_data.get("password")
            if usuario.pk == request.user.pk and password:
                update_session_auth_hash(request, usuario)
                messages.success(request, 'Tu contraseña ha sido actualizada correctamente. Tu sesión se ha mantenido activa.')
            else:
                messages.success(request, f"Usuario '{usuario.username}' actualizado correctamente.")

            return redirect('admin_panel')
    else:
        # Pass the request user to the form for validation logic
        form = UsuarioForm(instance=usuario, user=request.user)
        
    return render(request, 'form_usuarios.html', {'form': form, 'usuario': usuario})

@user_passes_test(lambda u: u.is_superuser)
def borrar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    return redirect('admin_panel')


def password_reset_flow(request):
    """
    Gestiona el flujo de restablecimiento de contraseña en una sola vista,
    utilizando la sesión para mantener el estado de forma segura.
    """
    # En una petición GET, siempre se muestra el primer paso.
    if request.method == 'GET':
        return render(request, 'login2.html', {'step': 1})

    # Para peticiones POST, se determina el paso actual.
    if 'check_phrase' in request.POST:
        # --- PASO 1: Verificar usuario y frase de seguridad ---
        username = request.POST.get('username')
        phrase = request.POST.get('frase_seguridad')
        
        try:
            # Búsqueda EXACTA por nombre de usuario para evitar ambigüedades.
            user = User.objects.get(username=username)
            # Validar que el perfil y la frase de seguridad coincidan EXACTAMENTE.
            if hasattr(user, 'perfil') and user.perfil.frase_seguridad == phrase:
                messages.success(request, 'Frase correcta. Ahora puedes establecer una nueva contraseña.')
                request.session['reset_user_pk'] = user.pk
                return render(request, 'login2.html', {'step': 2, 'username': user.username})
            else:
                # Mensaje de error genérico para no revelar si el usuario existe o no.
                messages.error(request, 'El nombre de usuario o la frase de seguridad no son correctos.')
                return render(request, 'login2.html', {'step': 1, 'username': username})
        except User.DoesNotExist:
            # Mensaje de error genérico.
            messages.error(request, 'El nombre de usuario o la frase de seguridad no son correctos.')
            return render(request, 'login2.html', {'step': 1, 'username': username})

    elif 'set_password' in request.POST:
        # --- PASO 2: Establecer la nueva contraseña ---
        user_pk = request.session.get('reset_user_pk')
        new_password = request.POST.get('new_password')
        
        if not user_pk or not new_password:
            messages.error(request, 'La sesión ha expirado o falta información. Por favor, inténtalo de nuevo.')
            return redirect('usuarios:password_reset_flow')

        try:
            user = User.objects.get(pk=user_pk)
            # Encriptar y guardar la nueva contraseña
            user.set_password(new_password)
            user.save()

            # Limpiar la variable de sesión para seguridad
            if 'reset_user_pk' in request.session:
                del request.session['reset_user_pk']

            # Redirigir al login en lugar de autologuear
            messages.success(request, '¡Contraseña actualizada con éxito! Ahora puedes iniciar sesión.')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'El usuario no fue encontrado. Por favor, inténtalo de nuevo.')
            return redirect('usuarios:password_reset_flow')
    
    # Si se recibe un POST no reconocido, se reinicia el flujo.
    return redirect('usuarios:password_reset_flow')


@user_passes_test(lambda u: u.is_superuser)
def toggle_user_active(request, user_id):
    if request.method == 'POST':
        user_to_toggle = get_object_or_404(User, id=user_id)
        if user_to_toggle != request.user:  # Un admin no puede desactivarse a sí mismo
            user_to_toggle.is_active = not user_to_toggle.is_active
            user_to_toggle.save()
            messages.success(request, f"El estado de '{user_to_toggle.username}' ha sido cambiado.")
        else:
            messages.error(request, "No puedes desactivar tu propia cuenta.")
    return redirect('admin_panel')

@user_passes_test(lambda u: u.is_superuser)
def toggle_user_staff(request, user_id):
    if request.method == 'POST':
        user_to_toggle = get_object_or_404(User, id=user_id)
        if user_to_toggle != request.user: # Un admin no puede quitarse a sí mismo el permiso de staff
            user_to_toggle.is_staff = not user_to_toggle.is_staff
            user_to_toggle.save()
            messages.success(request, f"Los permisos de '{user_to_toggle.username}' han sido cambiados.")
        else:
            messages.error(request, "No puedes quitar tus propios permisos de administrador.")
    return redirect('admin_panel')