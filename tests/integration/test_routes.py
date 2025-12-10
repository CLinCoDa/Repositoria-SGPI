import pytest
from app import app, db, initialize_data_once
from flask import url_for
import json

@pytest.fixture(scope="module")
def test_client():
    # Inicializamos los datos
    initialize_data_once(force=True)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ---------------------------------
# 1️⃣ Prueba de carga inicial
# ---------------------------------
def test_seed_data_loaded():
    assert len(db.users) >= 13
    assert len(db.convocatorias) >= 5
    assert len(db.solicitudes) >= 20

# ---------------------------------
# 2️⃣ Prueba de rutas protegidas
# ---------------------------------
def test_root_requires_login(test_client):
    response = test_client.get("/")
    assert response.status_code in (302, 401)  # redirect o json 401

def login_test_user(client):                                                                                                                                        
    # Asumimos que existe usuario admin
    admin = next(u for u in db.users if u["username"]=="admin")
    with client.session_transaction() as sess:
        sess["user_id"] = admin["id"]

# ---------------------------------
# 3️⃣ Prueba de listado de convocatorias
# ---------------------------------
def test_list_convocatorias(test_client):
    login_test_user(test_client)
    response = test_client.get("/convocatoria/")
    assert response.status_code == 200
    # contenido HTML debería contener al menos el nombre de una convocatoria
    html = response.data.decode("utf-8")
    assert "Convocatoria" in html

# ---------------------------------
# 4️⃣ Prueba de creación de convocatoria
# ---------------------------------
def test_create_convocatoria(test_client):
    login_test_user(test_client)
    data = {
        "tipo": "normal",
        "nombre": "Prueba Pytest",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-03-31",
        "estado": "planificada"
    }
    response = test_client.post("/convocatoria/crear", json=data)
    assert response.status_code == 200
    res_json = response.get_json()
    assert res_json["ok"] is True
    # Verificar que esté en la DB
    created = db.convocatorias[-1]
    assert created["nombre"] == "Prueba Pytest"

# ---------------------------------
# 5️⃣ Prueba de edición
# ---------------------------------
def test_edit_convocatoria(test_client):
    login_test_user(test_client)
    conv_id = db.convocatorias[-1]["id"]
    data = {"nombre": "Editada Pytest"}
    response = test_client.post(f"/convocatoria/editar/{conv_id}", json=data)
    assert response.status_code == 200
    assert db.get_convocatoria_by_id(conv_id)["nombre"] == "Editada Pytest"

# ---------------------------------
# 6️⃣ Prueba de eliminación
# ---------------------------------
def test_delete_convocatoria(test_client):
    login_test_user(test_client)
    conv_id = db.convocatorias[-1]["id"]
    response = test_client.delete(f"/convocatoria/eliminar/{conv_id}")
    assert response.status_code == 200
    assert db.get_convocatoria_by_id(conv_id) is None

# ---------------------------------
# 7️⃣ Prueba básica de filtros backend
# ---------------------------------
def test_filter_by_tipo():
    normal = [c for c in db.convocatorias if c["tipo"]=="normal"]
    extraordinaria = [c for c in db.convocatorias if c["tipo"]=="extraordinaria"]
    assert all(c["tipo"]=="normal" for c in normal)
    assert all(c["tipo"]=="extraordinaria" for c in extraordinaria)
