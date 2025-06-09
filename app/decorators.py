from functools import wraps
from flask import flash, redirect, request, url_for
from flask_login import current_user

def roles_requeridos(*roles_permitidos, mensaje=None, redireccion=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar autenticación y roles
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('auth.login', next=request.url))
                
            # Convertir roles a mayúsculas para comparación sin distinción de caso
            user_rol = current_user.get_rol().upper()
            roles_permitidos_upper = [r.upper() for r in roles_permitidos]
            
            if user_rol not in roles_permitidos_upper:
                # Mensaje personalizado o por defecto
                flash(mensaje or f'Se requieren los siguientes roles: {", ".join(roles_permitidos)}', 'error')
                # Redirección inteligente
                return redirect(redireccion or request.referrer or url_for('main.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator