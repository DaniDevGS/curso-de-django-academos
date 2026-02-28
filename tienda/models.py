from django.db import models
from app.models import BaseMode, Producto
from django.contrib.auth.models import User

class Compra(BaseMode):
    proveedor = models.CharField(max_length=150)
    total = models.DecimalField(decimal_places=2, default=0,max_digits=8) # type: ignore
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        # read_only_field = ["total"]

class CompraDetalle(BaseMode):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1,max_digits=8) # type: ignore
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)

class Venta(BaseMode):
    total = models.DecimalField(decimal_places=2, default=0,max_digits=8) # type: ignore
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

class VentaDetalle(BaseMode):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1,max_digits=8) # type: ignore
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "VentaDetalle"
        verbose_name_plural = "VentasDetalles"