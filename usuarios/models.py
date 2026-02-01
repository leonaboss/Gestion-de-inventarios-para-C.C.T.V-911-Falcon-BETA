from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore

class Perfil(models.Model):
	"""
	Modelo para extender el modelo de Usuario por defecto de Django.
	Aquí guardaremos la frase de seguridad.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
	frase_seguridad = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return f'Perfil de {self.user.username}'


@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
	"""
	Esta señal se asegura de que se cree un Perfil cada vez que se crea un User.
	"""
	Perfil.objects.get_or_create(user=instance)
