# routes/convocatorias_routes.py 

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from business_logic.services.convocatorias_service import (
    listar_convocatorias,
    crear_convocatoria,
    eliminar_convocatoria
)

convocatoria_bp = Blueprint("convocatorias", __name__, url_prefix="/convocatorias")

api_convocatoria_bp = Blueprint("api_convocatorias", __name__, url_prefix="/api/convocatorias")

# ---------------------------------------------------------
# GET /api/convocatorias  (con filtros)
# ---------------------------------------------------------
@convocatoria_bp.get("/")
def pagina_convocatorias():
    return render_template(
            "convocatorias/list.html", 
            current_year=datetime.now().year
        )

@api_convocatoria_bp.get("/")
def api_listar_convocatorias():
    filters = {
        "year": request.args.get("year"),
        "type": request.args.get("type"),
        "status": request.args.get("status"),
        "search": request.args.get("search")
    }

    
    convs = listar_convocatorias(filters)

    response = [c.to_dict() for c in convs]

    return jsonify(response)

# ---------------------------------------------------------
# POST /api/convocatorias
# ---------------------------------------------------------
@api_convocatoria_bp.post("/")
def api_crear_convocatoria():
    data = request.get_json()

    try:
        nueva = crear_convocatoria(data)
        return jsonify({
            "ok": True,
            "msg": "Convocatoria creada",
            "data": nueva.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 400


# ---------------------------------------------------------
# DELETE /api/convocatorias/<id>
# ---------------------------------------------------------
@api_convocatoria_bp.delete("/<int:conv_id>")
def api_eliminar_conv(conv_id):
    try:
        eliminar_convocatoria(conv_id)
        return jsonify({"ok": True, "msg": "Convocatoria eliminada"})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 400


