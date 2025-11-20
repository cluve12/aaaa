from django.contrib import admin
from .models import Sucursal, Cliente, Empleado, Proveedor, Producto, Pedido, DetallePedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'correo', 'mostrar_sucursales', 'foto_perfil_thumbnail']  # Cambiado
    list_filter = ['sucursales']  # Cambiado de 'sucursal' a 'sucursales'
    search_fields = ['nombre', 'correo']
    
    def mostrar_sucursales(self, obj):
        return ", ".join([sucursal.nombre for sucursal in obj.sucursales.all()])
    mostrar_sucursales.short_description = 'Sucursales'
    
    def foto_perfil_thumbnail(self, obj):
        if obj.foto_perfil:
            return f'<img src="{obj.foto_perfil.url}" style="width: 50px; height: 50px; object-fit: cover;" />'
        return "Sin foto"
    foto_perfil_thumbnail.allow_tags = True
    foto_perfil_thumbnail.short_description = 'Foto'

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'horario_apertura', 'horario_cierre', 'direccion']
    list_filter = ['nombre']
    search_fields = ['nombre', 'direccion']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puesto', 'sucursal', 'salario', 'fecha_contratacion']
    list_filter = ['sucursal', 'puesto']
    search_fields = ['nombre', 'puesto']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'telefono', 'correo', 'tipo_proveedor']
    list_filter = ['tipo_proveedor']
    search_fields = ['nombre', 'rfc']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'tipo', 'precio', 'calorias', 'proveedor', 'disponible']
    list_filter = ['tipo', 'proveedor', 'disponible']
    search_fields = ['nombre', 'descripcion']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'cliente', 'sucursal', 'fecha', 'total', 'estado', 'metodo_pago']
    list_filter = ['estado', 'sucursal', 'metodo_pago']
    search_fields = ['cliente__nombre', 'sucursal__nombre']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['producto__tipo']
    search_fields = ['pedido__id_pedido', 'producto__nombre']