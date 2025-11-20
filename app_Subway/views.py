from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Sucursal, Cliente, Empleado, Proveedor, Producto, Pedido, DetallePedido


# ==========================================
# FUNCIÓN PRINCIPAL - PÁGINA DE INICIO
# ==========================================
def inicio_subway(request):
    return render(request, 'app_Subway/inicio.html')

# ==========================================
# FUNCIONES PARA SUCURSALES
# ==========================================
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        horario_apertura = request.POST['horario_apertura']
        horario_cierre = request.POST['horario_cierre']
        direccion = request.POST['direccion']
        
        sucursal = Sucursal(
            nombre=nombre,
            telefono=telefono,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            direccion=direccion
        )
        
        if 'foto_sucursal' in request.FILES:
            sucursal.foto_sucursal = request.FILES['foto_sucursal']
        
        sucursal.save()
        return redirect('ver_sucursales')
    
    return render(request, 'app_Subway/sucursal/agregar_sucursal.html')

def ver_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/sucursal/ver_sucursales.html', {'sucursales': sucursales})

def detalle_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    clientes = sucursal.clientes.all()
    empleados = sucursal.empleados.all()
    
    # Obtener productos que han sido pedidos en esta sucursal
    productos = Producto.objects.filter(
        detallepedido__pedido__sucursal=sucursal
    ).distinct()[:4]
    
    # Obtener proveedores cuyos productos han sido pedidos en esta sucursal
    proveedores = Proveedor.objects.filter(
        productos__detallepedido__pedido__sucursal=sucursal
    ).distinct()[:4]
    
    return render(request, 'app_Subway/sucursal/detalle_sucursal.html', {
        'sucursal': sucursal,
        'clientes': clientes,
        'empleados': empleados,
        'productos': productos,
        'proveedores': proveedores
    })

def actualizar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    return render(request, 'app_Subway/sucursal/actualizar_sucursal.html', {'sucursal': sucursal})

def realizar_actualizacion_sucursal(request, id):
    if request.method == 'POST':
        sucursal = get_object_or_404(Sucursal, id=id)
        sucursal.nombre = request.POST['nombre']
        sucursal.telefono = request.POST['telefono']
        sucursal.horario_apertura = request.POST['horario_apertura']
        sucursal.horario_cierre = request.POST['horario_cierre']
        sucursal.direccion = request.POST['direccion']
        
        if 'foto_sucursal' in request.FILES:
            sucursal.foto_sucursal = request.FILES['foto_sucursal']
        
        sucursal.save()
        return redirect('ver_sucursales')
    
    return redirect('ver_sucursales')

def borrar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('ver_sucursales')
    
    return render(request, 'app_Subway/sucursal/borrar_sucursal.html', {'sucursal': sucursal})

# ==========================================
# FUNCIONES PARA PRODUCTOS Y PROVEEDORES EN SUCURSALES
# ==========================================
def productos_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    
    # Obtener productos que han sido pedidos en esta sucursal
    productos_pedidos = Producto.objects.filter(
        detallepedido__pedido__sucursal=sucursal
    ).distinct()
    
    context = {
        'sucursal': sucursal,
        'productos': productos_pedidos
    }
    return render(request, 'app_Subway/sucursal/productos_sucursal.html', context)

def proveedores_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    
    # Obtener proveedores cuyos productos han sido pedidos en esta sucursal
    proveedores = Proveedor.objects.filter(
        productos__detallepedido__pedido__sucursal=sucursal
    ).distinct()
    
    context = {
        'sucursal': sucursal,
        'proveedores': proveedores
    }
    return render(request, 'app_Subway/sucursal/proveedores_sucursal.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    context = {
        'producto': producto
    }
    return render(request, 'app_Subway/productos/detalle_producto.html', context)

# ==========================================
# FUNCIONES PARA EMPLEADOS
# ==========================================
def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'app_Subway/empleados/ver_empleados.html', {'empleados': empleados})

def agregar_empleado(request):
    if request.method == 'POST':
        sucursal_id = request.POST['sucursal']
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        salario = request.POST['salario']
        fecha_contratacion = request.POST['fecha_contratacion']
        puesto = request.POST['puesto']
        
        sucursal = get_object_or_404(Sucursal, id=sucursal_id)
        
        empleado = Empleado(
            sucursal=sucursal,
            nombre=nombre,
            telefono=telefono,
            salario=salario,
            fecha_contratacion=fecha_contratacion,
            puesto=puesto
        )
        
        if 'foto_perfil' in request.FILES:
            empleado.foto_perfil = request.FILES['foto_perfil']
        
        empleado.save()
        return redirect('ver_empleados')
    
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/empleados/agregar_empleado.html', {'sucursales': sucursales})

def actualizar_foto_perfil(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        if 'foto_perfil' in request.FILES:
            empleado.foto_perfil = request.FILES['foto_perfil']
            empleado.save()
            return redirect('ver_empleados')
    
    return render(request, 'app_Subway/empleados/actualizar_foto_perfil.html', {'empleado': empleado})

def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.telefono = request.POST['telefono']
        empleado.salario = request.POST['salario']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.puesto = request.POST['puesto']
        empleado.sucursal = get_object_or_404(Sucursal, id=request.POST['sucursal'])
        empleado.save()
        return redirect('ver_empleados')
    
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/empleados/actualizar_empleado.html', {
        'empleado': empleado,
        'sucursales': sucursales
    })

def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    
    return render(request, 'app_Subway/empleados/borrar_empleado.html', {'empleado': empleado})

# ==========================================
# FUNCIONES PARA CLIENTES
# ==========================================
def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_Subway/clientes/ver_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        print("=== DEBUG AGREGAR CLIENTE ===")
        print("Datos POST:", request.POST)
        print("Sucursales seleccionadas:", request.POST.getlist('sucursales'))
        
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        fecha_registro = request.POST['fecha_registro']
        sucursales_ids = request.POST.getlist('sucursales')
        
        print("Sucursales IDs:", sucursales_ids)
        
        cliente = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            fecha_registro=fecha_registro
        )
        
        if 'foto_perfil' in request.FILES:
            cliente.foto_perfil = request.FILES['foto_perfil']
        
        # GUARDAR PRIMERO
        cliente.save()
        print("Cliente guardado con ID:", cliente.id)
        
        # LUEGO ASIGNAR SUCURSALES
        if sucursales_ids:
            sucursales = Sucursal.objects.filter(id__in=sucursales_ids)
            print("Sucursales encontradas:", [s.nombre for s in sucursales])
            cliente.sucursales.set(sucursales)
            print("Sucursales asignadas al cliente")
        else:
            print("No se seleccionaron sucursales")
        
        # VERIFICAR
        cliente_verificado = Cliente.objects.get(id=cliente.id)
        print("Sucursales después de guardar:", [s.nombre for s in cliente_verificado.sucursales.all()])
        
        return redirect('ver_clientes')
    
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/clientes/agregar_cliente.html', {'sucursales': sucursales})

def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.direccion = request.POST['direccion']
        cliente.telefono = request.POST['telefono']
        cliente.correo = request.POST['correo']
        cliente.fecha_registro = request.POST['fecha_registro']
        
        if 'foto_perfil' in request.FILES:
            cliente.foto_perfil = request.FILES['foto_perfil']
        
        cliente.save()
        
        sucursales_ids = request.POST.getlist('sucursales')
        if sucursales_ids:
            sucursales = Sucursal.objects.filter(id__in=sucursales_ids)
            cliente.sucursales.set(sucursales)
        else:
            cliente.sucursales.clear()
        
        return redirect('ver_clientes')
    
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/clientes/actualizar_cliente.html', {
        'cliente': cliente,
        'sucursales': sucursales
    })

def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    
    return render(request, 'app_Subway/clientes/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# FUNCIONES PARA PROVEEDORES
# ==========================================
def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'app_Subway/proveedores/ver_proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST['direccion']
        rfc = request.POST['rfc']
        tipo_proveedor = request.POST['tipo_proveedor']
        
        proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            rfc=rfc,
            tipo_proveedor=tipo_proveedor
        )
        proveedor.save()
        return redirect('ver_proveedores')
    
    return render(request, 'app_Subway/proveedores/agregar_proveedor.html')

def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    
    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.telefono = request.POST['telefono']
        proveedor.correo = request.POST['correo']
        proveedor.direccion = request.POST['direccion']
        proveedor.rfc = request.POST['rfc']
        proveedor.tipo_proveedor = request.POST['tipo_proveedor']
        proveedor.save()
        return redirect('ver_proveedores')
    
    return render(request, 'app_Subway/proveedores/actualizar_proveedor.html', {'proveedor': proveedor})

def borrar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
    
    return render(request, 'app_Subway/proveedores/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# FUNCIONES PARA PRODUCTOS
# ==========================================
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'app_Subway/productos/ver_productos.html', {'productos': productos})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Proveedor

def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        tipo = request.POST['tipo']
        precio = request.POST['precio']
        calorias = request.POST['calorias']
        descripcion = request.POST['descripcion']
        proveedor_id = request.POST['proveedor']
        disponible = request.POST.get('disponible', False)
        
        proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
        
        producto = Producto(
            nombre=nombre,
            tipo=tipo,
            precio=precio,
            calorias=calorias,
            descripcion=descripcion,
            proveedor=proveedor,
            disponible=bool(disponible)
        )
        producto.save()
        return redirect('ver_productos')
    
    # Si no es POST, mostrar el formulario
    proveedores = Proveedor.objects.all()
    return render(request, 'app_Subway/products/agregar_producto.html', {'proveedores': proveedores})
    
    proveedores = Proveedor.objects.all()
    return render(request, 'app_Subway/productos/agregar_producto.html', {'proveedores': proveedores})

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.tipo = request.POST['tipo']
        producto.precio = request.POST['precio']
        producto.calorias = request.POST['calorias']
        producto.descripcion = request.POST['descripcion']
        producto.proveedor = get_object_or_404(Proveedor, id_proveedor=request.POST['proveedor'])
        producto.disponible = bool(request.POST.get('disponible', False))
        producto.save()
        return redirect('ver_productos')
    
    proveedores = Proveedor.objects.all()
    return render(request, 'app_Subway/productos/actualizar_producto.html', {
        'producto': producto,
        'proveedores': proveedores
    })

def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    
    return render(request, 'app_Subway/productos/borrar_producto.html', {'producto': producto})

# ==========================================
# FUNCIONES PARA PEDIDOS
# ==========================================
def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'app_Subway/pedidos/ver_pedidos.html', {'pedidos': pedidos})

def agregar_pedido(request):
    if request.method == 'POST':
        # Lógica para guardar el pedido (tu código actual)
        cliente_id = request.POST['cliente']
        sucursal_id = request.POST['sucursal']
        total = request.POST['total']
        estado = request.POST['estado']
        metodo_pago = request.POST['metodo_pago']
        notas = request.POST.get('notas', '')
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        sucursal = get_object_or_404(Sucursal, id=sucursal_id)
        
        pedido = Pedido(
            cliente=cliente,
            sucursal=sucursal,
            total=total,
            estado=estado,
            metodo_pago=metodo_pago,
            notas=notas
        )
        pedido.save()
        return redirect('ver_pedidos')
    
    else:
        # Lógica para mostrar el formulario (GET)
        productos = Producto.objects.filter(disponible=True)
        clientes = Cliente.objects.all()
        sucursales = Sucursal.objects.all()
        
        return render(request, 'empleados/pedidos/agregar_pedido.html', {
            'productos': productos,
            'clientes': clientes,
            'sucursales': sucursales
        })
    
    clientes = Cliente.objects.all()
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/pedidos/agregar_pedido.html', {
        'clientes': clientes,
        'sucursales': sucursales
    })

def detalle_pedido(request, id):
    pedido = get_object_or_404(Pedido, id_pedido=id)
    detalles = pedido.detalles.all()
    return render(request, 'app_Subway/pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })

def actualizar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id_pedido=id)
    
    if request.method == 'POST':
        pedido.cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        pedido.sucursal = get_object_or_404(Sucursal, id=request.POST['sucursal'])
        pedido.total = request.POST['total']
        pedido.estado = request.POST['estado']
        pedido.metodo_pago = request.POST['metodo_pago']
        pedido.notas = request.POST.get('notas', '')
        pedido.save()
        return redirect('ver_pedidos')
    
    clientes = Cliente.objects.all()
    sucursales = Sucursal.objects.all()
    return render(request, 'app_Subway/pedidos/actualizar_pedido.html', {
        'pedido': pedido,
        'clientes': clientes,
        'sucursales': sucursales
    })

def borrar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id_pedido=id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedidos')
    
    return render(request, 'app_Subway/pedidos/borrar_pedido.html', {'pedido': pedido})
# ==========================================
# FUNCIONES DE DEBUG (TEMPORALES)
# ==========================================

def debug_cliente_sucursal(request, cliente_id):
    """Función para debuggear un cliente específico"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    print(f"\n=== DEBUG CLIENTE: {cliente.nombre} ===")
    print(f"ID: {cliente.id}")
    print(f"Sucursales asociadas: {[s.nombre for s in cliente.sucursales.all()]}")
    print(f"Count: {cliente.sucursales.count()}")
    
    # Verificar en la base de datos directamente
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_Subway_cliente_sucursales WHERE cliente_id = %s", [cliente.id])
        rows = cursor.fetchall()
        print(f"Registros en tabla intermedia: {rows}")
    
    return redirect('ver_clientes')

def reparar_relaciones(request):
    """Función para reparar relaciones cliente-sucursal"""
    clientes = Cliente.objects.all()
    
    for cliente in clientes:
        print(f"\nReparando cliente: {cliente.nombre}")
        sucursales_actuales = cliente.sucursales.all()
        print(f"Sucursales actuales: {[s.nombre for s in sucursales_actuales]}")
        
        # Forzar una actualización
        cliente.save()
        print("Cliente guardado nuevamente")
        
        # Verificar después de guardar
        cliente_refreshed = Cliente.objects.get(id=cliente.id)
        print(f"Sucursales después: {[s.nombre for s in cliente_refreshed.sucursales.all()]}")
    
    return redirect('ver_clientes')

def prueba_rapida(request):
    """Crear un cliente de prueba con sucursales"""
    from django.utils import timezone
    
    # Crear cliente
    cliente = Cliente(
        nombre="CLIENTE PRUEBA DEBUG",
        direccion="Dirección prueba DEBUG",
        telefono="1234567890",
        correo="prueba@debug.com",
        fecha_registro=timezone.now().date()
    )
    cliente.save()
    print(f"=== CLIENTE PRUEBA CREADO CON ID: {cliente.id} ===")
    
    # Obtener algunas sucursales
    sucursales = Sucursal.objects.all()[:2]  # Primeras 2 sucursales
    
    if sucursales:
        cliente.sucursales.set(sucursales)
        print(f"Cliente prueba asociado a: {[s.nombre for s in sucursales]}")
        
        # Verificar inmediatamente
        cliente_verificado = Cliente.objects.get(id=cliente.id)
        print(f"VERIFICACIÓN: {[s.nombre for s in cliente_verificado.sucursales.all()]}")
    else:
        print("ERROR: No hay sucursales para asociar")
    
    return redirect('ver_clientes')

def ver_todos_clientes(request):
    """Ver todos los clientes y sus sucursales"""
    clientes = Cliente.objects.all()
    
    print("\n" + "="*50)
    print("DEBUG: TODOS LOS CLIENTES Y SUS SUCURSALES")
    print("="*50)
    
    for cliente in clientes:
        sucursales = cliente.sucursales.all()
        print(f"\nCliente: {cliente.nombre} (ID: {cliente.id})")
        print(f"Sucursales: {[s.nombre for s in sucursales]}")
        print(f"Total: {sucursales.count()} sucursales")
    
    print("\n" + "="*50)
    
    return redirect('ver_clientes')