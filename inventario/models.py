from django.db import models  # type: ignore[import]
from django.contrib.auth.models import User  # type: ignore[import]
from django.utils import timezone  # type: ignore[import]
from decimal import Decimal


class Cantidad(models.Model):
    valor = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.valor)


class Codigo(models.Model):
    valor = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.valor


class NumeroDeBien(models.Model):
    valor = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.valor


class CodBien(models.Model):
    valor = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.valor


class Descripcion(models.Model):
    texto = models.TextField(blank=True, null=True)

    def __str__(self):
        return (self.texto or '')[:50]


class Concepto(models.Model):
    texto = models.TextField(blank=True, null=True)

    def __str__(self):
        return (self.texto or '')[:50]


class ValorUnitario(models.Model):
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    moneda = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"{self.valor} {self.moneda}"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)

    # Orden solicitado y campos legados fijados para compatibilidad con formularios/plantillas
    cantidad = models.IntegerField(default=0)
    codigo = models.CharField(max_length=100, blank=True, null=True)        # CODIGO
    num_de_bien = models.CharField(max_length=100, blank=True, null=True)   # NumDeBien
    descripcion = models.TextField(blank=True, null=True)
    cod_bien = models.CharField(max_length=100, blank=True, null=True)      # CodBien
    concepto = models.TextField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # FKs normalizadas (opcional, mantienen compatibilidad y permiten relacionar entidades)
    cantidad_obj = models.ForeignKey(Cantidad, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    codigo_obj = models.ForeignKey(Codigo, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    num_de_bien_obj = models.ForeignKey(NumeroDeBien, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    descripcion_obj = models.ForeignKey(Descripcion, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    cod_bien_obj = models.ForeignKey(CodBien, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    concepto_obj = models.ForeignKey(Concepto, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    valor_unitario_obj = models.ForeignKey(ValorUnitario, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    fecha_agregado = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # sincronizar cantidad (producto.cantidad <-> producto.cantidad_obj)
        if self.cantidad is not None:
            if self.cantidad_obj is None or self.cantidad_obj.valor != self.cantidad:
                # Si no hay objeto Cantidad o difiere, asegurar existencia y link
                cantidad_obj, _ = Cantidad.objects.get_or_create(valor=self.cantidad)
                self.cantidad_obj = cantidad_obj
        elif self.cantidad_obj:
            self.cantidad = self.cantidad_obj.valor

        # sincronizar codigo
        if self.codigo:
            codigo_obj, _ = Codigo.objects.get_or_create(valor=self.codigo)
            self.codigo_obj = codigo_obj
        elif self.codigo_obj and (not self.codigo or self.codigo != self.codigo_obj.valor):
            self.codigo = self.codigo_obj.valor

        # sincronizar num_de_bien
        if self.num_de_bien:
            num_obj, _ = NumeroDeBien.objects.get_or_create(valor=self.num_de_bien)
            self.num_de_bien_obj = num_obj
        elif self.num_de_bien_obj and (not self.num_de_bien or self.num_de_bien != self.num_de_bien_obj.valor):
            self.num_de_bien = self.num_de_bien_obj.valor

        # sincronizar descripcion
        if self.descripcion:
            desc_obj, _ = Descripcion.objects.get_or_create(texto=self.descripcion)
            self.descripcion_obj = desc_obj
        elif self.descripcion_obj and (not self.descripcion or self.descripcion != self.descripcion_obj.texto):
            self.descripcion = self.descripcion_obj.texto

        # sincronizar cod_bien
        if self.cod_bien:
            cod_obj, _ = CodBien.objects.get_or_create(valor=self.cod_bien)
            self.cod_bien_obj = cod_obj
        elif self.cod_bien_obj and (not self.cod_bien or self.cod_bien != self.cod_bien_obj.valor):
            self.cod_bien = self.cod_bien_obj.valor

        # sincronizar concepto
        if self.concepto:
            concepto_obj, _ = Concepto.objects.get_or_create(texto=self.concepto)
            self.concepto_obj = concepto_obj
        elif self.concepto_obj and (not self.concepto or self.concepto != self.concepto_obj.texto):
            self.concepto = self.concepto_obj.texto

        # sincronizar valor_unitario
        if self.valor_unitario is not None:
            if self.valor_unitario_obj is None or self.valor_unitario_obj.valor != self.valor_unitario:
                vu_obj, _ = ValorUnitario.objects.get_or_create(valor=self.valor_unitario)
                self.valor_unitario_obj = vu_obj
        elif self.valor_unitario_obj:
            self.valor_unitario = self.valor_unitario_obj.valor

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Soft delete: marcar como inactivo en lugar de borrar
        self.activo = False
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.activo = True
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.nombre


class TipoMovimiento(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('edicion', 'Edición'),
        ('INACTIVO', 'Salida'),
        ('restaurar', 'Restaurar'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)

    def __str__(self):
        return self.tipo


class Movimiento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Actualiza stock solo al crear (no al editar)
        if not self.pk:
            if self.producto and not self.producto.activo:
                raise ValueError('No se puede registrar un movimiento en un producto inactivo.')

            if self.tipo_movimiento.tipo == 'entrada':
                self.producto.cantidad += self.cantidad
            elif self.tipo_movimiento.tipo == 'salida':
                if self.producto.cantidad < self.cantidad:
                    raise ValueError('No hay suficiente stock para realizar la salida.')
                self.producto.cantidad -= self.cantidad
            self.producto.save()

            # Mantener sincronía con cantidad_obj también
            if self.producto.cantidad_obj:
                self.producto.cantidad_obj.valor = self.producto.cantidad
                self.producto.cantidad_obj.save()
        super().save(*args, **kwargs)

    def __str__(self):
        prod_name = self.producto.nombre if self.producto else '(Sin producto)'
        return f"{self.tipo_movimiento.tipo} - {prod_name} ({self.cantidad})"