from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('borrar/<int:user_id>/', views.borrar_usuario, name='borrar_usuario'),
    
    # URL unificada para el flujo de restablecimiento de contraseña
    path('recuperar-cuenta/', views.password_reset_flow, name='password_reset_flow'),

    # URLs para acciones de superusuario
    path('toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('toggle-staff/<int:user_id>/', views.toggle_user_staff, name='toggle_user_staff'),
]
