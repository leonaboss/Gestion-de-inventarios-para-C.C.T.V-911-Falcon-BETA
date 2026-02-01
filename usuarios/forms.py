from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UsuarioForm(forms.ModelForm):
    """
    Formulario para que un administrador cree o edite usuarios.
    La lógica de guardado (incluida la contraseña y la frase de seguridad)
    está contenida en el método `save` de este formulario.
    """
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False, help_text="Dejar en blanco para no cambiar la contraseña.")
    frase_seguridad = forms.CharField(max_length=255, required=False, help_text="Frase para recuperación de cuenta.")

    is_staff = forms.BooleanField(
        label='Es administrador',
        required=False,
        help_text='Permite que este usuario gestione el sistema y acceda al panel de control.'
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        # Store the user making the request, if available.
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If creating a new user (no instance), password is required
        if not self.instance or not self.instance.pk:
            self.fields['password'].required = True
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'perfil'):
            self.fields['frase_seguridad'].initial = self.instance.perfil.frase_seguridad
        
        # El campo de contraseña no debe mostrar la contraseña hasheada
        self.fields['password'].initial = ''

    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get("is_active")
        is_staff = cleaned_data.get("is_staff")

        # Prevent an admin from deactivating their own account via this form
        is_editing_self = self.request_user and self.instance and self.request_user.pk == self.instance.pk
        
        # This check is now more robust. It only triggers if the user is editing
        # themselves AND the 'is_active' field was explicitly changed to False.
        if is_editing_self and 'is_active' in self.changed_data and not is_active:
            raise forms.ValidationError(
                "No puedes desactivar tu propia cuenta desde este formulario. "
                "Contacta a otro administrador si necesitas desactivarla.",
                code='self_deactivation'
            )
        
        # Prevent an admin from revoking their own staff status
        if is_editing_self and 'is_staff' in self.changed_data and not is_staff:
            raise forms.ValidationError(
                "No puedes revocar tu propio estado de administrador. "
                "Contacta a otro superusuario si es necesario.",
                code='self_staff_revocation'
            )
            
        return cleaned_data


    def save(self, commit=True):
        # Primero, obtenemos el objeto de usuario que se va a guardar,
        # sin confirmarlo aún en la base de datos.
        # super().save(commit=False) se encarga de los campos del modelo User.
        user = super().save(commit=False)

        # Ahora, manejamos la contraseña.
        # Si el campo de contraseña tiene un valor, lo hasheamos y lo asignamos.
        password_from_form = self.cleaned_data.get("password")
        if password_from_form:
            user.set_password(password_from_form)


        # Si commit es True, guardamos el usuario y el perfil.
        if commit:
            user.save()

            # Manejamos la frase de seguridad.
            # La señal post_save ya ha garantizado que user.perfil exista.
            if 'frase_seguridad' in self.cleaned_data:
                # La frase de seguridad puede estar vacía.
                frase = self.cleaned_data.get("frase_seguridad", "")
                # No necesitamos get_or_create porque la señal en models.py
                # ya ha creado el perfil.
                user.perfil.frase_seguridad = frase
                user.perfil.save()

        return user


class PublicUsuarioForm(forms.ModelForm):
    """
    Formulario para el registro público de nuevos usuarios.
    """
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    frase_seguridad = forms.CharField(max_length=255, help_text="Esta frase se usará para recuperar tu cuenta.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Los nuevos usuarios públicos se crean como activos por defecto para acceso inmediato.
        user.is_active = True
        
        if commit:
            user.save()
            # Se usa get_or_create para crear el perfil de forma segura y explícita.
            frase = self.cleaned_data.get('frase_seguridad', '')
            perfil, created = Perfil.objects.get_or_create(user=user)
            perfil.frase_seguridad = frase
            perfil.save()
            
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """AuthenticationForm personalizado para mensajes en español y manejo de usuario inactivo."""
    error_messages = {
        'invalid_login': _("Por favor introduce un usuario y contraseña correctos."),
        'inactive': _("Tu cuenta está inactiva. Contacta con un administrador para activarla."),
    }

    def confirm_login_allowed(self, user):
        """Asegura que si el usuario existe pero está inactivo, se muestre el mensaje 'inactive'."""
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')