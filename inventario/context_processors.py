from .models import Producto, Movimiento
from django.contrib.auth import get_user_model
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def sidebar_metrics(request):
    """
    Procesador de contexto para inyectar métricas clave en todas las plantillas.
    """
    # Métricas de Bienes
    total_bienes_activos = Producto.objects.filter(activo=True).count()
    total_bienes_inactivos = Producto.objects.filter(activo=False).count()
    
    # Métrica de Valor Total
    valor_total_inventario = Producto.objects.filter(activo=True).aggregate(
        total=Coalesce(Sum('valor_unitario'), Value(0), output_field=DecimalField())
    )['total']

    # Métricas de Movimientos
    total_movimientos = Movimiento.objects.count()
    fecha_limite_recientes = timezone.now() - timedelta(days=7)
    movimientos_recientes = Movimiento.objects.filter(fecha__gte=fecha_limite_recientes).count()

    # Métrica de Usuarios
    total_usuarios = User.objects.count()

    return {
        'total_bienes_activos': total_bienes_activos,
        'total_bienes_inactivos': total_bienes_inactivos,
        'valor_total_inventario': valor_total_inventario,
        'total_movimientos': total_movimientos,
        'movimientos_recientes': movimientos_recientes,
        'total_usuarios': total_usuarios,
    }
