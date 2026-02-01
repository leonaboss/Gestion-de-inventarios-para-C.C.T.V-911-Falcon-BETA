from django.urls import path
from . import views
from usuarios import views as usuarios_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bienes/', views.inventario, name='inventario'),
    path('bienes-ocultos/', views.bienes_ocultos, name='bienes_ocultos'),
    path('bienes-inactivos/', views.bienes_inactivos, name='bienes_inactivos'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('exportar/excel/', views.export_productos_excel, name='export_productos_excel'),
    path('importar/excel/', views.importar_productos_excel, name='importar_productos_excel'),
    path('ocultar/<int:producto_id>/', views.ocultar_producto, name='ocultar_producto'),
    path('restaurar/<int:producto_id>/', views.restaurar_producto, name='restaurar_producto'),
    path('historial/', views.historial_view, name='historial'),
    path('historial/limpiar/', views.limpiar_historial_movimientos, name='limpiar_historial_movimientos'),
    path('usuarios/toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('usuarios/log/', views.user_log_view, name='usuarios_log'),
    path('usuarios/log/limpiar/', views.limpiar_historial_usuarios, name='limpiar_historial_usuarios'),
    path('usuarios/toggle-staff/<int:user_id>/', views.toggle_user_staff, name='toggle_user_staff'),
    path('usuarios/crear/', usuarios_views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:user_id>/', usuarios_views.editar_usuario, name='editar_usuario'),
    path('usuarios/borrar/<int:user_id>/', usuarios_views.borrar_usuario, name='borrar_usuario'),
]