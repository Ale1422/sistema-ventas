from flask import render_template, jsonify, redirect, url_for, flash, request, session
from ..admin.models import Producto
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

@empleado_bp.route("/empleado", methods=["GET"])
def dashboard():
    total = sum(item['subtotal'] for item in session.get('carrito', []))
    return render_template('empleado/index.html', carrito=session['carrito'], Producto = Producto, total = total)

@empleado_bp.route('/buscar_producto', methods=['GET'])
def buscar_producto():
    termino = request.args.get('q', '')
    productos = Producto.query.filter(Producto.Nombre_Producto.ilike(f'%{termino}%')).all()
    productos_json = [{'id': p.id, 'nombre': p.Nombre_Producto, 'precio': p.Precio} for p in productos]
    return jsonify(productos_json)

@empleado_bp.route('/venta', methods=['GET'])
def venta():
    # Inicializamos el carrito en la sesión si no existe
    if 'carrito' not in session:
        session['carrito'] = []

    total = sum(float(item['subtotal']) for item in session.get('carrito', []))
    # Mostrar listado de productos y carrito
    return render_template('empleado/index.html', carrito=session['carrito'], Producto = Producto, total = total)


@empleado_bp.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    producto_id = request.json.get('producto_id')
    cantidad = int(request.json.get('cantidad', 1))

    # Obtener el producto de la base de datos
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Inicializar el carrito si no existe
    carrito = session.get('carrito', [])
    print(carrito)

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

@empleado_bp.route('/detalle_venta/<int:venta_id>')
def detalle_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    detalles = DetalleVenta.query.filter_by(ID_Venta=venta_id).all()
    return render_template('empleado/detalle_venta.html', venta=venta, detalles=detalles)


@empleado_bp.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    producto_id = request.json.get('producto_id')

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
def generar_venta():
    usuario_id = current_user.id # Obtén el ID del usuario logueado
    metodo_pago = 'Efectivo'  # Aquí puedes definir o permitir que el usuario seleccione el método de pago
    descuento = float('0.00')  # Define el descuento, si existe

    # Obtener el carrito desde la sesión o la base de datos
    carrito = session.get('carrito', [])

    if not carrito:
        flash('El carrito está vacío.')
        return redirect(url_for('empleado.venta'))

    # Llamar a la función para registrar la venta y los detalles
    try:
        venta_id = registrar_venta(usuario_id, carrito, metodo_pago, descuento)
        # Vaciar el carrito después de la venta
        session['carrito'] = []
        flash('Venta generada exitosamente.')
        return redirect(url_for('empleado.detalle_venta', venta_id=venta_id))  # Redirigir a una página de detalle de la venta
    except Exception as e:
        db.session.rollback()
        print(str(e))
        flash(f'Ocurrió un error al generar la venta: {str(e)}')
        return redirect(url_for('empleado.venta'))


@empleado_bp.route('/calcular_total', methods=['POST'])
def calcular_total():
    total = sum(item['subtotal'] for item in session.get('carrito', []))
    return render_template('empleado/venta.html', carrito=session['carrito'], total=total)


@empleado_bp.route('/limpiar_carrito')
def limpiar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('empleado.venta'))