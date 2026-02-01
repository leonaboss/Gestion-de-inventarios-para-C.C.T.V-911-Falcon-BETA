from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from .models import Perfil

# Define un "inline" para el modelo Perfil.
# Esto permite editar el Perfil dentro de la página del Usuario.
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'

# Define una nueva clase de UserAdmin que incluye el PerfilInline
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Vuelve a registrar el modelo User con el nuevo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


