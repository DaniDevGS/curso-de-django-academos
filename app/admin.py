from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from unfold.admin import ModelAdmin
from .models import Producto, Categoria

def dashboard_callback(request, context):

    categorias_data = Categoria.objects.annotate(
        total=Count('producto')
    ).values('nombre', 'total')
    
    valor_total_inventario = Producto.objects.aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    context.update({
        "cards": [
            {
                "title": "Total Productos",
                "metric": Producto.objects.count(),
                "footer": "Productos en el catálogo",
            },
            {
                "title": "Categorías",
                "metric": Categoria.objects.count(),
                "footer": "Categorías activas",
            },
            {
                "title": "Stock Total",
                "metric": Producto.objects.aggregate(total=Sum('cantidad'))['total'] or 0,
                "footer": "Unidades en inventario",
            },
            {
                "title": "Valor Inventario",
                "metric": f"${valor_total_inventario:,.2f}",
                "footer": "Suma total de precios",
            },
        ],
        "charts": [
            {
                "title": "Productos por Categoría",
                "type": "pie",
                "labels": [c['nombre'] for c in categorias_data if c['total'] > 0],
                "data": [c['total'] for c in categorias_data if c['total'] > 0],
            }
        ],
    })
    return context


@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ("nombre_con_badge", "descripcion_corta", "total_productos", "fecha_creacion_formateada")
    search_fields = ("nombre", "descripcion")
    list_filter = ("fecha_creacion",)
    
    def nombre_con_badge(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4px 8px; border-radius: 4px;">{}</span>',
            obj.nombre
        )
    nombre_con_badge.short_description = "Categoría"
    
    def descripcion_corta(self, obj):
        if obj.descripcion:
            return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
        return "-"
    descripcion_corta.short_description = "Descripción"
    
    def total_productos(self, obj):
        count = obj.producto_set.count()
        return format_html(
            '<span class="bg-green-600/20 text-green-400 px-3 py-1 rounded-full text-xs font-bold">{}</span>',
            count
        )
    total_productos.short_description = "Productos"
    
    def fecha_creacion_formateada(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y %H:%M")
    fecha_creacion_formateada.short_description = "Creado"


@admin.register(Producto)
class ProductoAdmin(ModelAdmin):
    list_display = (
        'nombre_con_badge',
        'categoria_estilizada',
        'precio_formateado',
        'stock_con_color',
        'fecha_creacion_formateada'
    )
    list_filter = ('categoria', 'fecha_creacion')
    list_editable = ()
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Inventario y Precios', {
            'fields': ('cantidad', 'precio')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',),
        }),
    )
    
    def nombre_con_badge(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #fff;">{}</span>',
            obj.nombre
        )
    nombre_con_badge.short_description = "Producto"
    
    def categoria_estilizada(self, obj):
        if not obj.categoria:
            return format_html('<span class="text-slate-500 italic">Sin categoría</span>')
        return format_html(
            '<span class="bg-primary-600/20 text-primary-400 px-2 py-1 rounded-md text-xs font-bold border border-primary-500/30">{}</span>',
            obj.categoria.nombre
        )
    categoria_estilizada.short_description = "Categoría"
    
    def precio_formateado(self, obj):
        # CORREGIDO: Formateamos el número antes de pasarlo a format_html
        precio_formateado = "${:,.2f}".format(obj.precio)
        return format_html(
            '<span class="font-bold text-green-400">{}</span>',
            precio_formateado
        )
    precio_formateado.short_description = "Precio"
    
    def stock_con_color(self, obj):
        if obj.cantidad <= 0:
            return format_html(
                '<span class="bg-red-600/20 text-red-400 px-2 py-1 rounded-md text-xs font-bold border border-red-500/30">🔴 Sin stock</span>'
            )
        elif obj.cantidad < 10:
            return format_html(
                '<span class="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded-md text-xs font-bold border border-yellow-500/30">🟡 {} uds.</span>',
                obj.cantidad
            )
        else:
            return format_html(
                '<span class="bg-green-600/20 text-green-400 px-2 py-1 rounded-md text-xs font-bold border border-green-500/30">🟢 {} uds.</span>',
                obj.cantidad
            )
    stock_con_color.short_description = "Stock"
    
    def descripcion_corta(self, obj):
        if obj.descripcion:
            return obj.descripcion[:60] + "..." if len(obj.descripcion) > 60 else obj.descripcion
        return format_html('<span class="text-slate-500 italic">Sin descripción</span>')
    descripcion_corta.short_description = "Descripción"
    
    def fecha_creacion_formateada(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y")
    fecha_creacion_formateada.short_description = "Creado"
    fecha_creacion_formateada.admin_order_field = 'fecha_creacion'
    