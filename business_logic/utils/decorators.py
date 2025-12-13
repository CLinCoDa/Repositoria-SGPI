from flask import session, redirect, url_for, flash, request, jsonify
from functools import wraps

# Asume que 'db.get_user(user_id)' devuelve el objeto de usuario con el campo 'role'
from data_layer.database.database import db # Asegúrate de que db es accesible

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Para API (JSON), podrías devolver un 401
            if request.blueprint and request.blueprint.startswith('api_'):
                return jsonify({"ok": False, "msg": "No autorizado"}), 401
                
            # Para páginas (HTML), redirige al login
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    return decorated_function

def rol_required(rol_necesario):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                # Si no está logueado, redirige a login (o 401 para API)
                return redirect(url_for('login')) # O devuelve 401

            user = db.get_user_by_id(user_id) # Debes implementar esta función
            if not user or user.get("role") != rol_necesario:
                # No tiene el rol. Devuelve 403 (Prohibido)
                if request.blueprint and request.blueprint.startswith('api_'):
                    return jsonify({"ok": False, "msg": "Acceso Prohibido"}), 403
                    
                flash("No tienes permiso para acceder a esta función.", "danger")
                return redirect(url_for('home')) # Redirige a una página segura o de error
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator