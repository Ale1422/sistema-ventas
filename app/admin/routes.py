from flask import render_template, redirect, url_for, request, flash, jsonify
from ..decorators import roles_requeridos
from werkzeug.urls import url_parse
from .models import Producto
from ..auth.models import User, Rol
from .forms import ProductoForm, EditarProductoForm, SignupForm, EditarUsuarioForm
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError

from . import admin_bp


@admin_bp.route("/admin", methods=["GET"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def dashboard():
    try:
        return render_template('admin/dashboard.html')
    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route("/usuario", methods=["GET", "POST"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def mostrar_usuarios():
    try:
        form = SignupForm()
        error = None
        usuarios = User.get_all()
        rolesDb = Rol.query.with_entities(Rol.id, Rol.Nombre_Rol).order_by(Rol.id.desc()).all()
        roles = []
        for rol in rolesDb:
            roles.append((rol.id, rol.Nombre_Rol))

        form.rol.choices = roles  

        if form.validate_on_submit():
            name = form.name.data
            lastName = form.lastName.data
            rol = form.rol.data
            email = form.email.data
            password = form.password.data
            
            # Comprobamos que no hay ya un usuario con ese email
            user = User.get_by_email(email)
            if user is not None:
                error = f'El email {email} ya está siendo utilizado por otro usuario'
            else:
                # Creamos el usuario y lo guardamos
                user = User(nombre = name, apellido = lastName, email = email, idRol= rol)
                user.set_password(password)
                user.save()
                # Dejamos al usuario logueado
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('admin.mostrar_usuarios')
                return redirect(next_page)
        return render_template("admin/listado_usuarios.html", usuarios = usuarios, form=form, error=error)

    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

@admin_bp.route("/editarUsuario/<id_usuario>", methods=['POST', 'GET'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def editar_usuario(id_usuario):
    try:
        id = id_usuario
        user = User.get_by_id(id)
        form = EditarUsuarioForm(obj=user)

        rolesDb = Rol.query.with_entities(Rol.id, Rol.Nombre_Rol).order_by(Rol.id.desc()).all()
        roles = []
        for rol in rolesDb:
            roles.append((rol.id, rol.Nombre_Rol))

        form.rol.choices = roles

        if form.validate_on_submit():
            user.nombre = form.nombre.data
            user.apellido = form.apellido.data
            user.rol = form.rol.data
            user.email = form.email.data
            user.save()
            flash('Se edito correctamente!', 'success')
            return redirect(url_for('admin.mostrar_usuarios')) 
            

        return render_template('admin/editar-usuario.html', form=form)
    
    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

@admin_bp.route("/admin/cambiar_estado/<int:id_usuario>", methods=['POST'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def cambiar_estado_usuario(id_usuario):
    try:
        user = User.get_by_id(id_usuario)
        
        if not user:
            flash('No se encontro el usuario!', 'warning')
            return redirect(url_for('admin.productos'))

        # Lógica de alternancia (Switch)
        nuevo_estado = 'inactivo' if user.estado == 'activo' else 'activo'
        user.estado = nuevo_estado
        user.save()
        flash('Se cambio el estado correctamente!', 'success')

        return redirect(url_for('admin.mostrar_usuarios'))
    
    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.mostrar_usuarios'))

@admin_bp.route("/admin/productos", methods=["GET", "POST"])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def productos():
    try:
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

    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.productos'))
    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.productos'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.productos'))    
    

@admin_bp.route('/edit/<id>', methods=['POST', 'GET'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def get_contact(id):
    try:
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
    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.productos'))
    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.productos'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.productos'))

@admin_bp.route('/cambiar_estado_producto/<id>', methods=['POST'])
@roles_requeridos("ADMINISTRADOR", mensaje='Solo para administradores', redireccion='/')
def cambiar_estado_producto(id):
    try:
        producto = Producto.get_by_id(id)
        
        if not producto:
            flash('No se encontro el producto!', 'warning')
            return redirect(url_for('admin.productos'))

        # Lógica de alternancia (Switch)
        nuevo_estado = 'disponible' if producto.Estado == 'no disponible' else 'no disponible'
        producto.Estado = nuevo_estado
        producto.save() # Asumo que tu método save() hace el commit a la DB
        flash('Se cambio el estado correctamente!', 'success')

        return redirect(url_for('admin.productos'))
    
    except IntegrityError as e:
        # Error común: Clave única duplicada (ej. email ya existe) o error de llave foránea
        print(f"Error de Integridad: {e}") 
        flash('Error: El dato ya existe o viola una restricción (ej. Email duplicado).', 'error')
        return redirect(url_for('admin.productos'))
    except DataError as e:
        # Error común: Datos demasiado largos para la columna o tipo incorrecto
        print(f"Error de Datos: {e}")
        flash('Error: Formato de datos incorrecto (ej. texto muy largo).', 'error')
        return redirect(url_for('admin.productos'))

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('admin.productos'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('admin.productos'))