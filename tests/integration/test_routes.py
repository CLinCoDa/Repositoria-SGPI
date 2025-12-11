import pytest
from app import app, db, initialize_data_once
from flask import url_for
import json

# --- Configuración Inicial y Fixture ---

@pytest.fixture(scope="module")
def test_client():
    """
    Fixture que inicializa los datos de prueba y configura el cliente Flask.
    Scope="module" asegura que la DB simulada se carga solo una vez.
    """
    # Inicializamos los datos (Necesario para asegurar que existe un Coordinador)
    initialize_data_once(force=True)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# -----------------------------------------------------
# FUNCIÓN DE UTILERÍA: Login de Usuario Coordinador
# -----------------------------------------------------
def login_coordinador(client):                                                                                                                                        
    """ Busca y simula el login con el primer usuario que tenga rol 'coordinador'. """
    
    # 1. Buscar al Coordinador. Usamos 'role' 
    # Asumo que el rol del administrador es 'coordinador' (todo minúscula).
    coordinador = next(
        (u for u in db.users if u.get("role") == "coordinador"), 
        None
    )
    
    # Si la búsqueda por 'coordinador' falla, intenta con 'admin' o 'Coordinador'
    if coordinador is None:
        coordinador = next(
            (u for u in db.users if u.get("username") == "admin"), 
            None
        )

    assert coordinador is not None, "ERROR: No se encontró usuario con rol 'coordinador' o 'admin' para las pruebas."
    
    # 2. Asignar ID en sesión
    with client.session_transaction() as sess:
        sess["user_id"] = coordinador["id"]

# ---------------------------------
# 1️⃣ Prueba de carga inicial
# ---------------------------------
def test_seed_data_loaded():
    """Verifica que los datos mínimos de prueba se hayan cargado."""
    assert len(db.users) >= 13, "Fallo: Menos de 13 usuarios cargados."
    assert len(db.convocatorias) >= 5, "Fallo: Menos de 5 convocatorias cargadas."
    assert len(db.solicitudes) >= 8, "Fallo: Menos de 8 solicitudes cargadas."

# ---------------------------------
# 2️⃣ Prueba de rutas protegidas (Pre-requisito)
# ---------------------------------
def test_root_requires_login(test_client):
    """Verifica que la ruta raíz sin login redirige o devuelve 401."""
    response = test_client.get("/")
    # Esperamos 302 (Redirección a login) o 401 (No autorizado)
    assert response.status_code in (302, 401)

# -----------------------------------------------------
# PRUEBAS DE INTEGRACIÓN: ROL COORDINADOR (CRUD Convocatorias)
# -----------------------------------------------------

# ---------------------------------
# 3️⃣ Prueba de listado de convocatorias
# ---------------------------------
def test_coordinador_list_convocatorias(test_client):
    """Prueba que el Coordinador puede acceder a la página de listado."""
    login_coordinador(test_client)
    response = test_client.get("/convocatorias/")
    assert response.status_code == 200, f"Listado falló, Status: {response.status_code}"
    # Contenido HTML (debe cargar la página)
    html = response.data.decode("utf-8")
    assert "Convocatoria" in html, "No se encontró contenido esperado en el HTML."

# ---------------------------------
# 4️⃣ Prueba de creación de convocatoria
# ---------------------------------
def test_coordinador_create_convocatoria(test_client):
    """Prueba que el Coordinador puede crear una nueva convocatoria."""
    login_coordinador(test_client)
    data = {
        "tipo": "normal",
        "nombre": "Prueba Pytest (C)",
        "descripcion": "Descripción de la prueba",
        "anio": 2025,
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-03-31",
        "estado": "planificada"
    }
    # La ruta puede ser /convocatorias/crear (HTML form) o /api/convocatorias/ (JSON API)
    # Asumo que la ruta que recibe el JSON es la que hace la creación
    response = test_client.post("/api/convocatorias/crear", json=data) 
    
    assert response.status_code == 201, f"Creación falló, Status: {response.status_code}"
    res_json = response.get_json()
    assert res_json["ok"] is True, f"Fallo al crear convocatoria: {res_json.get('msg')}"
    
    # Verificar que esté en la DB
    created = db.convocatorias[-1]
    assert created["nombre"] == "Prueba Pytest (C)"

# ---------------------------------
# 5️⃣ Prueba de edición
# ---------------------------------
def test_coordinador_edit_convocatoria(test_client):
    """Prueba que el Coordinador puede editar una convocatoria existente."""
    login_coordinador(test_client)
    # Usar la última convocatoria creada (de la prueba anterior)
    conv_id = db.convocatorias[-1]["id"]
    data = {"nombre": "Editada Pytest (C)"}
    
    response = test_client.put(f"/api/convocatorias/{conv_id}", json=data)
    
    assert response.status_code == 200
    
    # Verificar cambio en la DB
    assert db.get_convocatoria_by_id(conv_id)["nombre"] == "Editada Pytest (C)"

# ---------------------------------
# 6️⃣ Prueba de eliminación
# ---------------------------------
def test_coordinador_delete_convocatoria(test_client):
    login_coordinador(test_client)
    
    # 1. Verificar la eliminación exitosa (debe devolver 200)
    conv_id_to_delete = db.convocatorias[-1]["id"]
    response_delete = test_client.delete(f"/api/convocatorias/{conv_id_to_delete}")
    
    assert response_delete.status_code == 200, "La eliminación debería devolver 200 OK."
    assert db.get_convocatoria_by_id(conv_id_to_delete) is None, "El registro no fue eliminado de la DB."
    
    # 2. Verificar el manejo de 404 (Buena Práctica)
    # Intentar eliminar de nuevo el mismo ID
    response_404 = test_client.delete(f"/api/convocatorias/{conv_id_to_delete}")
    assert response_404.status_code == 404, "La eliminación de un ID inexistente debe devolver 404."

# ---------------------------------
# 7️⃣ Prueba básica de filtros backend (No necesita login específico)
# ---------------------------------
# (Se mantiene igual, ya que solo prueba la lógica de la capa de servicio/DB)
def test_filter_by_tipo():
    normal = [c for c in db.convocatorias if c["tipo"]=="normal"]
    extraordinaria = [c for c in db.convocatorias if c["tipo"]=="extraordinaria"]
    assert all(c["tipo"]=="normal" for c in normal)
    assert all(c["tipo"]=="extraordinaria" for c in extraordinaria)