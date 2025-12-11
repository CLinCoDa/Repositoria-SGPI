# routes/solicitudes_routes.py 

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from business_logic.services.solicitudes_service import (
    listar_solicitudes,
    crear_solicitud,
    eliminar_solicitud
)
from business_logic.services.convocatorias_service import (
    listar_convocatorias
)

solicitudes_bp = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")

api_solicitudes_bp = Blueprint("api_solicitudes", __name__, url_prefix="/api/solicitudes")

# ---------------------------------------------------------
# GET /solicitudes/
# Renderiza la vista principal de la tabla de solicitudes
# ---------------------------------------------------------
@solicitudes_bp.get("/")
def pagina_registro():

    # Se asume que listar_convocatorias() devuelve solo las activas o todas, 
    # y son necesarias para poblar el filtro en el HTML.
    convocatorias_activas = listar_convocatorias()

    return render_template(
            "solicitudes/list.html", 
            convocatorias=convocatorias_activas
        )

# ---------------------------------------------------------
# GET /api/solicitudes/ (con filtros)
# ---------------------------------------------------------
@api_solicitudes_bp.get("/")
def api_listar_solicitudes():
    
    # 1. Recoger filtros (se usan los nombres de las variables JS)
    raw_filters = {
        "estado": request.args.get("estado"),
        "convocatoria_id": request.args.get("convocatoria_id"),
        "tipo_pi": request.args.get("tipo_pi"),
        "search": request.args.get("search")
    }

    # 2. Limpiar filtros: remover valores None o cadenas vacías
    filters = {k: v for k, v in raw_filters.items() if v} 

    convs = listar_convocatorias()

    convocatoria_map = {c.id: c.nombre for c in convs}
    
    solics = listar_solicitudes(filters)

    # Nota: Se asume que 'solics' es una lista de objetos Solicitud con método to_dict()
    response = []
    for soli in solics:
        # Convertir el objeto Solicitud (limpio) a diccionario
        soli_dict = soli.to_dict()
        
        # Obtener el nombre usando el ID del mapa
        conv_id = soli_dict.get('convocatoria_id')
        nombre = convocatoria_map.get(conv_id, 'N/A')
        
        # Añadir el campo de vista (convocatoria_nombre) al diccionario
        soli_dict['convocatoria_nombre'] = nombre
        
        response.append(soli_dict)
        
    # --- 5. Devolver la respuesta enriquecida ---
    return jsonify(response)

# ---------------------------------------------------------
# GET /solicitudes/crear
# Renderiza la vista del formulario de creación
# ---------------------------------------------------------
@solicitudes_bp.get("/crear")
def pagina_crear_solicitud():
    return render_template(
            "solicitudes/create.html", 
        )


# ---------------------------------------------------------
# POST /api/solicitudes/
# Crea una nueva solicitud via API
# ---------------------------------------------------------
@api_solicitudes_bp.post("/")
def api_crear_solicitud():
    data = request.get_json()

    try:
        nueva = crear_solicitud(data)
        return jsonify({
            "ok": True,
            "msg": "Solicitud creada",
            "data": nueva.to_dict()
        }), 201
    except Exception as e:
        # En producción, solo retornar un mensaje genérico.
        print(f"Error al crear solicitud: {e}") 
        return jsonify({"ok": False, "msg": str(e)}), 400


# ---------------------------------------------------------
# DELETE /api/solicitudes/<id>
# Elimina una solicitud via API
# ---------------------------------------------------------
@api_solicitudes_bp.delete("/<int:soli_id>")
def api_eliminar_solicitud(soli_id): # <--- CORRECCIÓN DE NOMBRE
    try:
        eliminar_solicitud(soli_id) # <--- CORRECCIÓN DE NOMBRE
        return jsonify({"ok": True, "msg": "Solicitud eliminada"})
    except Exception as e:
        print(f"Error al eliminar solicitud ID {soli_id}: {e}")
        return jsonify({"ok": False, "msg": str(e)}), 400
