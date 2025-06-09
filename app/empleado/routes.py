from flask import render_template, jsonify, redirect, url_for, flash, request, session
from ..admin.models import Producto
from ..decorators import roles_requeridos
from flask_login import current_user
from app import db

from .models import Venta, DetalleVenta
from datetime import datetime

from . import empleado_bp

def registrar_venta(usuario_id, carrito, metodo_pago, descuento=float('0.00')):
    # Calcular el total de la venta sumando los subtotales de cada producto en el carrito
    total_venta = sum(float(item['subtotal']) for item in carrito) - descuento

    # Crear la venta
    nueva_venta = Venta(
        usuario_id,
        datetime.utcnow(),
        total_venta,
        metodo_pago,
        descuento
    )
    db.session.add(nueva_venta)
    db.session.flush()  # Realiza una operación parcial para obtener el ID de la venta

    # Agregar detalles de venta
    for item in carrito:
        detalle = DetalleVenta(
            nueva_venta.id,  # ID de la venta recién creada
            item['id'],
            item['cantidad'],
            item['precio_unitario'],
            item['subtotal']
        )
        db.session.add(detalle)

    # Confirmar los cambios en la base de datos
    db.session.commit()
    return nueva_venta.id

@empleado_bp.route('/venta', methods=['GET'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def venta():
    # Inicializamos el carrito en la sesión si no existe
    if 'carrito' not in session:
        session['carrito'] = []

    total = sum(float(item['subtotal']) for item in session.get('carrito', []))

    return render_template('empleado/index.html', carrito=session['carrito'], Producto = Producto, total = total, fecha_actual = datetime.now().strftime('%d-%m-%Y'))

@empleado_bp.route('/agregar-producto', methods=['POST'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def agregar_producto():
    producto_id = request.json.get('producto_id')
    cantidad = int(request.json.get('cantidad', 1))

    # Obtener el producto de la base de datos
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Inicializar el carrito si no existe
    carrito = session.get('carrito', [])

    # Buscar si el producto ya está en el carrito
    producto_en_carrito = next((item for item in carrito if item['id'] == producto_id), None)

    if producto_en_carrito:
        # Si el producto ya está en el carrito, actualiza la cantidad y el subtotal
        producto_en_carrito['cantidad'] += cantidad
        producto_en_carrito['subtotal'] = producto_en_carrito['cantidad'] * producto.Precio
    else:
        # Si no está en el carrito, añadir el producto como un nuevo item
        nuevo_item = {
            'id': producto_id,
            'codigo': producto_id + 1000,
            'nombre': producto.Nombre_Producto,
            'cantidad': cantidad,
            'precio_unitario': producto.Precio,
            'subtotal': producto.Precio * cantidad
        }
        carrito.append(nuevo_item)

    # Actualizar el carrito en la sesión
    session['carrito'] = carrito

    # Calcular el total
    total = sum(float(item['subtotal']) for item in carrito)

    # Enviar la respuesta con el carrito actualizado y el nuevo total
    return jsonify({'carrito': carrito, 'total': total})

@empleado_bp.route('/buscar_producto', methods=['GET'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def buscar_producto():
    termino = request.args.get('q', '')
    codigo = request.args.get('codigo', None)
    productos = None
    if(codigo):
        codigo = int(codigo) - 1000
        productos = Producto.query.filter(Producto.id.ilike(f'%{codigo}%')).all()
    else:
        productos = Producto.query.filter(Producto.Nombre_Producto.ilike(f'%{termino}%')).all()
    productos_json = [{'id': p.id, 'nombre': p.Nombre_Producto, 'precio': p.Precio} for p in productos]
    return jsonify(productos_json)

@empleado_bp.route('/producto/<int:id_producto>', methods=['GET'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def producto_id(id_producto):

    if(id_producto):
        producto = Producto.get_by_id(id_producto)

    return jsonify({'id': producto.id, 'nombre': producto.Nombre_Producto, 'precio': producto.Precio})

@empleado_bp.route('/detalle_venta/<int:venta_id>')
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def detalle_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    detalles = DetalleVenta.query.filter_by(ID_Venta=venta_id).all()
    
    # Formatear ID con ceros a la izquierda (6 dígitos)
    venta_id_formateado = f"{venta.id:06d}"
    
    return render_template('empleado/detalle_venta.html', 
                        venta=venta, 
                        detalles=detalles,
                        venta_id_formateado=venta_id_formateado)

@empleado_bp.route('/listado_ventas', methods = ['GET'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def listado_ventas():
        # Obtener las fechas de los parámetros GET
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # Construir la consulta base
    query = Venta.query

    # Aplicar filtro de fechas si están especificadas
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        query = query.filter(Venta.Fecha_Venta >= fecha_inicio)
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        query = query.filter(Venta.Fecha_Venta <= fecha_fin)
    
    # Ejecutar la consulta
    ventas = query.all()

    # Renderizar el template y pasar las ventas filtradas
    return render_template('empleado/listado_ventas.html', ventas=ventas)


@empleado_bp.route('/eliminar_producto', methods=['POST'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def eliminar_producto():
    producto_id = int(request.json.get('producto_id'))

    # Recuperar el carrito de la sesión
    carrito = session.get('carrito', [])

    # Filtrar el carrito para eliminar el producto con el ID dado
    carrito = [item for item in carrito if item['id'] != producto_id]
    session['carrito'] = carrito  # Actualizar el carrito en la sesión

    # Calcular el nuevo total
    total = sum(float(item['subtotal']) for item in carrito)

    # Enviar el carrito actualizado y el nuevo total
    return jsonify({'carrito': carrito, 'total': total})

@empleado_bp.route('/generar_venta', methods=['POST'])
@roles_requeridos("EMPLEADO", mensaje='Solo para empleados', redireccion='/')
def generar_venta():
    usuario_id = current_user.id
    metodo_pago = request.form.get('metodo_pago', 'efectivo')
    detalle_venta = request.form.get('detalle_venta', '')
    descuento = float('0.00')

    carrito = session.get('carrito', [])

    if not carrito:
        flash('El carrito está vacío.', 'error')
        return redirect(url_for('empleado.venta'))

    try:
        venta_id = registrar_venta(usuario_id, carrito, metodo_pago, descuento)
        
        # Si necesitas guardar el detalle adicional en la venta
        venta = Venta.query.get(venta_id)
        venta.Detalle = detalle_venta  # Asegúrate de tener este campo en tu modelo
        db.session.commit()
        
        session['carrito'] = []
        flash('Venta generada exitosamente.', 'success')
        return redirect(url_for('empleado.detalle_venta', venta_id=venta_id))
    except Exception as e:
        db.session.rollback()
        print(str(e))
        flash(f'Ocurrió un error al generar la venta: {str(e)}', 'error')
        return redirect(url_for('empleado.venta'))
