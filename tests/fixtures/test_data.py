# test_app.py
from app import app, db, initialize_data_once

def test_seed_data():
    # Inicializar seed de datos
    initialize_data_once(force=True)
    
    # Revisar que los usuarios se cargaron
    assert len(db.users) > 0, "No se cargaron usuarios"
    print(f"Usuarios cargados: {len(db.users)}")

    # Revisar convocatorias
    assert len(db.convocatorias) > 0, "No se cargaron convocatorias"
    print(f"Convocatorias cargadas: {len(db.convocatorias)}")

    # Revisar solicitudes
    assert len(db.solicitudes) > 0, "No se cargaron solicitudes"
    print(f"Solicitudes cargadas: {len(db.solicitudes)}")

def test_flask_routes():
    # Crear cliente de pruebas
    with app.test_client() as client:
        # Ruta protegida: debe redirigir al login
        res = client.get("/")
        assert res.status_code in [302, 401], "Ruta protegida no protegida"
        print("Ruta '/' protegida correctamente")

        # Ruta de listado de convocatorias (sin login, debería dar 302 o 401)
        res2 = client.get("/convocatoria/")
        assert res2.status_code in [302, 401], "Listado convocatorias accesible sin login"
        print("Ruta '/convocatoria/' protegida correctamente")

        # Simular login: asignar user_id en sesión
        with client.session_transaction() as sess:
            sess["user_id"] = db.users[0]["id"]

        # Ahora debería devolver 200
        res3 = client.get("/")
        assert res3.status_code == 200, "Ruta protegida no funciona con login"
        print("Ruta '/' funciona correctamente con login")

if __name__ == "__main__":
    test_seed_data()
    test_flask_routes()
    print("Pruebas básicas completadas ✅")
