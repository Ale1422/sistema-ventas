from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from app import login_manager
from . import auth_bp
from .forms import LoginForm
from .models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('public.index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)
            if user is not None and user.estado == 'inactivo':
                flash('Su usuario se encuentra deshabilitado', 'warning')
            elif user is not None and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    if user.get_rol() == "ADMINISTRADOR":
                        next_page = url_for('admin.dashboard')
                    else:
                        next_page = url_for('empleado.venta')
                return redirect(next_page)
            else:
                flash('No se encontro usuario', 'warning')

        return render_template('auth/login_form.html', form=form)

    except OperationalError as e:
        # Error común: La base de datos está caída, no responde o error de conexión
        print(f"Error Operacional: {e}")
        flash('Error: Fallo de conexión con la base de datos.', 'error')
        return redirect(url_for('public'))

    except SQLAlchemyError as e:
        # Captura cualquier otro error general de SQLAlchemy que no sea los anteriores
        print(f"Error General SQLAlchemy: {e}")
        flash('Ocurrió un error inesperado en la base de datos.', 'error')
        return redirect(url_for('public'))

    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('public'))


@auth_bp.route('/logout')
def logout():
    try:
        logout_user()
        return redirect(url_for('public.index'))
    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
        return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(int(user_id))
    except Exception as e:
        print(e)
        flash('Ups, algo sucedio!', 'error')
