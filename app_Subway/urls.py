from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio_subway, name='inicio'),
    
    # URLs para Sucursales
    path('sucursales/agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('sucursales/', views.ver_sucursales, name='ver_sucursales'),
    path('sucursales/detalle/<int:id>/', views.detalle_sucursal, name='detalle_sucursal'),
    path('sucursales/actualizar/<int:id>/', views.actualizar_sucursal, name='actualizar_sucursal'),
    path('sucursales/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_sucursal, name='realizar_actualizacion_sucursal'),
    path('sucursales/borrar/<int:id>/', views.borrar_sucursal, name='borrar_sucursal'),
    
    # URLs para Productos y Proveedores en Sucursales
    path('sucursales/<int:sucursal_id>/productos/', views.productos_sucursal, name='productos_sucursal'),
    path('sucursales/<int:sucursal_id>/proveedores/', views.proveedores_sucursal, name='proveedores_sucursal'),
    path('producto/<int:producto_id>/detalle/', views.detalle_producto, name='detalle_producto'),
    
    # URLs para Empleados
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/actualizar-foto/<int:id>/', views.actualizar_foto_perfil, name='actualizar_foto_perfil'),
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # URLs para Clientes
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # URLs para Proveedores
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/borrar/<int:id>/', views.borrar_proveedor, name='borrar_proveedor'),
    
    # URLs para Productos
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/borrar/<int:id>/', views.borrar_producto, name='borrar_producto'),
    
    # URLs para Pedidos (FALTANTES - AGREGAR ESTAS)
    path('pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedidos/detalle/<int:id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/actualizar/<int:id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedidos/borrar/<int:id>/', views.borrar_pedido, name='borrar_pedido'),

    # Agrega estas líneas a tu urlpatterns:
path('debug/cliente/<int:cliente_id>/', views.debug_cliente_sucursal, name='debug_cliente'),
path('reparar/relaciones/', views.reparar_relaciones, name='reparar_relaciones'),
path('prueba/rapida/', views.prueba_rapida, name='prueba_rapida'),
path('debug/todos-clientes/', views.ver_todos_clientes, name='ver_todos_clientes'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)