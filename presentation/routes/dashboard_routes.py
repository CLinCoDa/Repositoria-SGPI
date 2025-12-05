# presentation/routes/dashboard_routes.py

from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Ruta protegida: solo usuarios logueados pueden entrar
@dashboard_bp.route("/")
def dashboard_home():
    # Verificar login   
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    return render_template("dashboard/dashboard.html")
