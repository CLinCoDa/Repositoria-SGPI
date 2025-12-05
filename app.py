# app.py
from flask import Flask, request, session, redirect, url_for, jsonify
from data_layer.database.database import db
from data_layer.database.seed_data import seed_users, seed_convocatorias, seed_solicitudes
from presentation.routes.auth_routes import auth_bp
from presentation.routes.dashboard_routes import dashboard_bp
from presentation.routes.convocatorias_routes import convocatoria_bp

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_en_produccion"

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(convocatoria_bp)

# Rutas públicas para ejemplo
PUBLIC_ENDPOINTS = {
    "auth.login_page",
    "auth.login",
    "auth.logout",
    "static"
}

# Protección simple de rutas
@app.before_request
def require_login():
    # request.endpoint puede ser None en ciertas condiciones
    ep = request.endpoint
    if ep is None or ep in PUBLIC_ENDPOINTS:
        return
    if "user_id" not in session:
        # Si es API JSON, devolver 401; si no, redirigir al login.
        accept = request.headers.get("Accept", "")
        if "application/json" in accept:
            return jsonify({"ok": False, "msg": "autenticación requerida"}), 401
        return redirect(url_for("auth.login_page"))

# Ruta protegida de ejemplo
@app.get("/")
def protected_index():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login_page"))
    user = db.get_user_by_id(user_id)
    return f"<h3>Bienvenido {user.get('full_name', user.get('username'))}</h3><p>Role: {user.get('role')}</p><a href='/auth/logout'>Logout</a>"




# Inicializar datos seed UNA VEZ al arranque (Flask 3.x no tiene before_first_request)
def initialize_data_once(persist_to_disk: bool = False, force: bool = False):
    """
    Inserta datos seed si la DB está vacía o si 'force' es True.
    Llamar desde app startup (antes de app.run).
    """
    if db.users and not force:
        return

    # Semillas
    for u in seed_users():
        db.add_user(u)

    # Convocatorias
    for c in seed_convocatorias():
        db.add_convocatoria(c)

    # Solicitudes: si deseas asociar user_id/convocatoria_id válidos
    # aqui hacemos un mapeo simple (asignamos user_id aleatorio entre docentes)
    import random
    docentes = [u for u in db.users if u.get("role") == "docente"]
    convocatoria_ids = [c["id"] for c in db.convocatorias] or [None]
    for s in seed_solicitudes():
        # asignar user_id aleatorio si hay docentes
        if docentes:
            s["user_id"] = random.choice(docentes)["id"]
        else:
            s["user_id"] = db.users[0]["id"] if db.users else None
        s["convocatoria_id"] = random.choice(convocatoria_ids) if convocatoria_ids else None
        db.add_solicitud(s)

if __name__ == "__main__":
    # Opcional: persist_to_disk True si quieres guardar en data/
    # Nota: si cambias persist_to_disk, recrea db con get_database(persist_to_disk=True)
    # aquí usamos el db singleton ya importado
    initialize_data_once()
    app.run(debug=True, port=5000)
