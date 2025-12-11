# routes/convocatorias_routes.py 

from flask import Blueprint, request, jsonify, render_template, current_app
from datetime import datetime
from business_logic.utils.decorators import login_required, rol_required
from business_logic.services.convocatorias_service import (
    listar_convocatorias,
    crear_convocatoria,
    editar_convocatoria,
    eliminar_convocatoria
)

convocatoria_bp = Blueprint("convocatorias", __name__, url_prefix="/convocatorias")

api_convocatoria_bp = Blueprint("api_convocatorias", __name__, url_prefix="/api/convocatorias")

# ---------------------------------------------------------
# GET /api/convocatorias  (con filtros)
# ---------------------------------------------------------
@convocatoria_bp.get("/")
@rol_required('coordinador')
def pagina_convocatorias():
    return render_template(
            "convocatorias/list.html", 
            current_year=datetime.now().year
        )

@api_convocatoria_bp.get("/")
@login_required
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
@api_convocatoria_bp.post("/crear")
@rol_required('coordinador')
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
        return jsonify({"ok": False, "msg": str(e)}), 500


@api_convocatoria_bp.put("/<int:conv_id>")
@rol_required('coordinador')
def api_editar_convocatoria(conv_id):
    data = request.get_json()

    try:
        convocatoria_actualizada = editar_convocatoria(conv_id, data)
        
        # 1. Manejar 404 Not Found (Si la capa de servicio devuelve None)
        if convocatoria_actualizada is None:
            return jsonify({"ok": False, "msg": f"Convocatoria con ID {conv_id} no encontrada"}), 404
        
        # 2. Respuesta Exitosa (200 OK)
        return jsonify({
            "ok": True,
            "msg": "Convocatoria actualizada",
            "data": convocatoria_actualizada.to_dict()
        }), 200
        
    # 3. Manejar 400 Bad Request (Si la capa de servicio lanza un error de validación)
    # except ValidationError as e:
    #     return jsonify({"ok": False, "msg": str(e)}), 400
    
    # 4. Manejar 500 Internal Server Error (Errores inesperados)
    except Exception as e:
        current_app.logger.error(f"Error al actualizar convocatoria {conv_id}: {e}")
        return jsonify({"ok": False, "msg": "Error interno del servidor"}), 500

# ---------------------------------------------------------
# DELETE /api/convocatorias/<id>
# ---------------------------------------------------------
@api_convocatoria_bp.delete("/<int:conv_id>")
@rol_required('coordinador')
def api_eliminar_conv(conv_id):
    try:
        # Llama al servicio, que retorna True o False
        eliminado_con_exito = eliminar_convocatoria(conv_id) 
        
        # 1. Chequeo de Éxito (True)
        if eliminado_con_exito:
            return jsonify({
                "ok": True, 
                "msg": f"Convocatoria con ID {conv_id} eliminada"
            }), 200 # <-- Éxito
        
        # 2. Chequeo de No Encontrado (False)
        else:
            # Si el servicio retorna False, significa que la convocatoria no existía.
            return jsonify({
                "ok": False, 
                "msg": f"Convocatoria con ID {conv_id} no encontrada para eliminar"
            }), 404 # <-- No encontrado
            
    except Exception as e:
        # 3. Fallo Inesperado (500 o 400 si es un error de código/validación)
        return jsonify({"ok": False, "msg": str(e)}), 500


