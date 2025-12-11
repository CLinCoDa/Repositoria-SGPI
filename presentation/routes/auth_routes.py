# presentation/routes/auth_routes.py
from flask import Blueprint, request, session, render_template,redirect, jsonify, url_for
from data_layer.database.database import db
from business_logic.utils.password_utils import verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Página de login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("auth/login.html")

# Procesar login desde JS
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form or request.get_json() or {}

    # Tu JS envía "usuario"
    username = data.get("usuario") or data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Debe ingresar usuario y contraseña."
        }), 400

    user = db.find_user_by_username(username)
    if not user:
        return jsonify({
            "success": False,
            "message": "Usuario no encontrado."
        }), 404

    if not verify_password(password, user.get("password_hash", "")):
        return jsonify({
            "success": False,
            "message": "Contraseña incorrecta."
        }), 401

    # Login exitoso
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["email"] = user["email"]

    return jsonify({
        "success": True,
        "message": "Inicio de sesión exitoso",
        "redirect": url_for("dashboard.dashboard_home")
    })

    #return redirect(url_for("dashboard.dashboard_home"))

# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return render_template("auth/login.html")

