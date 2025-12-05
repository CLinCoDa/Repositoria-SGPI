from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicie sesión para acceder a esta página')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*required_roles):
    """Decorador para requerir roles específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor inicie sesión')
                return redirect(url_for('auth.login_page'))
            
            user_role = session.get('role')
            if user_role not in required_roles:
                flash('No tiene permisos para acceder a esta página')
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Uso en las rutas:
# @login_required
# @roles_required('administrador', 'gestor')