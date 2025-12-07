from flask import render_template, redirect, url_for, request, flash
from ..decorators import roles_requeridos
from werkzeug.urls import url_parse
from .models import Producto
from ..auth.models import User
from .forms import ProductoForm,EditarProductoForm, SignupForm

from . import admin_bp


@admin_bp.route("/admin", methods=["GET"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route("/signup/", methods=["GET", "POST"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def show_signup_form():
    form = SignupForm()
    error = None
    usuarios = User.get_all()
    if form.validate_on_submit():
        name = form.name.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(nombre = name, apellido = lastName, email = email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
    return render_template("admin/signup_form.html", usuarios = usuarios, form=form, error=error)

@admin_bp.route("/admin/productos", methods=["GET", "POST"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def productos():
    form = ProductoForm()
    productos = Producto.get_all()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        precio = form.precio.data
        stock = form.stock.data

        nuevoProducto = Producto(nombre, descripcion, precio, stock)
        nuevoProducto.save()

        return redirect(url_for('admin.productos'))    

    return render_template('admin/productos.html', form=form, productos = productos)

@admin_bp.route('/edit/<id>', methods=['POST', 'GET'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def get_contact(id):
    producto = Producto.get_by_id(id)
    form = EditarProductoForm(obj=producto)

    if form.validate_on_submit():
        producto.Nombre_producto = form.Nombre_Producto.data
        producto.Descripción = form.Descripción.data
        producto.Precio = form.Precio.data
        producto.Stock_Cantidad = form.Stock_Cantidad.data
        producto.save()
        flash('Se edito correctamente!', 'success')
        return redirect(url_for('admin.productos')) 
        

    return render_template('admin/editar-producto.html', form=form)

@admin_bp.route('/cambiar_estado_producto/<id>', methods=['POST'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def cambiar_estado_producto(id):
    producto = Producto.get_by_id(id)
    if producto:
        producto.Estado = 'disponible' if producto.Estado == 'no disponible' else 'no disponible'
        producto.save()
        flash('Se cambio el estado correctamente!', 'success')
        return redirect(url_for('admin.productos'))
    return redirect(url_for('admin.productos'))