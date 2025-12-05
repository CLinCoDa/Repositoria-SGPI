from flask import Blueprint, request, session, render_template,redirect, jsonify, url_for
from data_layer.database.database import db
from business_logic.utils.password_utils import verify_password

convocatoria_bp = Blueprint("convocatoria", __name__, url_prefix="/convocatoria")

@convocatoria_bp.get("/")
def convocatoria_list():
    convocatorias = db.convocatorias  # lista completa
    return render_template("convocatorias/list.html", convocatorias=convocatorias)


@convocatoria_bp.get("/detalle/<int:convocatoria_id>")
def convocatoria_detalle(convocatoria_id):
    conv = db.get_convocatoria(convocatoria_id)

    if not conv:
        return jsonify({"ok": False, "msg": "Convocatoria no encontrada"}), 404
    
    return jsonify({"ok": True, "data": conv})

@convocatoria_bp.post("/crear")
def convocatoria_create():
    data = request.form or request.get_json() or {}

    tipo = data.get("tipo")
    nombre = data.get("nombre")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    estado = data.get("estado", "planificada")

    if not tipo or not nombre or not fecha_inicio or not fecha_fin:
        return jsonify({"ok": False, "msg": "Todos los campos son obligatorios"}), 400

    nueva = db.add_convocatoria({
        "tipo": tipo,
        "nombre": nombre,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "estado": estado,
    })

    return jsonify({"ok": True, "msg": "Convocatoria creada", "data": nueva})

@convocatoria_bp.post("/editar/<int:convocatoria_id>")
def convocatoria_update(convocatoria_id):
    data = request.form or request.get_json() or {}

    conv = db.get_convocatoria(convocatoria_id)
    if not conv:
        return jsonify({"ok": False, "msg": "Convocatoria no encontrada"}), 404

    updates = {
        "nombre": data.get("nombre", conv["nombre"]),
        "tipo": data.get("tipo", conv["tipo"]),
        "fecha_inicio": data.get("fecha_inicio", conv["fecha_inicio"]),
        "fecha_fin": data.get("fecha_fin", conv["fecha_fin"]),
        "estado": data.get("estado", conv["estado"]),
    }

    db.update_convocatoria(convocatoria_id, updates)

    return jsonify({"ok": True, "msg": "Convocatoria actualizada"})


@convocatoria_bp.delete("/eliminar/<int:convocatoria_id>")
def convocatoria_delete(convocatoria_id):
    ok = db.delete_convocatoria(convocatoria_id)

    if not ok:
        return jsonify({"ok": False, "msg": "No existe"}), 404

    return jsonify({"ok": True, "msg": "Convocatoria eliminada"})

