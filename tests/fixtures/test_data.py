# test_app.py
from app import app, db, initialize_data_once

# ... (otras funciones de prueba) ...

def test_flask_routes():
    # Asegúrate de que los datos de prueba se hayan cargado antes de correr esta prueba
    if not db.users:
        initialize_data_once(force=True)

    # 1. ENCONTRAR UN USUARIO CON EL ROL REQUERIDO (COORDINADOR)
    #    Asumimos que el rol se almacena en la clave 'rol' o similar.
    #    Necesitas ajustar la condición ('rol' == 'Coordinador') según la estructura real de tu objeto de usuario.
    coordinador = None
    for user in db.users:
        if user.get("role") == "coordinador": # <-- AJUSTA ESTA CONDICIÓN
            coordinador = user
            break
            
    assert coordinador is not None, "Error: No se encontró ningún usuario con rol 'Coordinador' en los datos de prueba."
    
    # 2. CREAR CLIENTE DE PRUEBAS
    with app.test_client() as client:
        # ... (Tus pruebas de rutas protegidas sin login) ...
        # (Estas permanecen igual, comprueban que *sin* login, las rutas fallan)
        
        # Ruta protegida: debe redirigir al login
        res = client.get("/")
        assert res.status_code in [302, 401], "Ruta protegida no protegida"
        print("Ruta '/' protegida correctamente")

        # Ruta de listado de convocatorias (sin login)
        res2 = client.get("/convocatorias/")
        assert res2.status_code in [302, 401], "Listado convocatorias accesible sin login"
        print("Ruta '/convocatorias/' protegida correctamente")

        # 3. SIMULAR LOGIN CON EL USUARIO COORDINADOR ENCONTRADO
        with client.session_transaction() as sess:
            sess["user_id"] = coordinador["id"] # <-- USAMOS EL ID DEL COORDINADOR

        # 4. AHORA DEBERÍA DEVOLVER 200 (Y ACCEDER A RUTAS DE COORDINADOR)
        
        # Ruta '/' (funciona para cualquier usuario logueado)
        res3 = client.get("/")
        assert res3.status_code == 302, "Ruta '/' no redirige después del login."
        
        # 2. Verificar que el destino de la redirección es correcto
        assert res3.headers.get('Location') == "/dashboard/", "Ruta '/' redirige a un lugar incorrecto."
        
        print("Ruta '/' funciona correctamente (redirige a /dashboard/)")
        
        # Ruta de listado de convocatorias (Solo accesible para Coordinador)
        # Esto debería solucionar el FAILED tests/integration/test_routes.py::test_list_convocatorias
        res4 = client.get("/convocatorias/")
        assert res4.status_code == 200, "Listado convocatorias no funciona con login de coordinador"
        print("Ruta '/convocatorias/' funciona correctamente con login de coordinador")
        
# ... (Bloque if __name__ == "__main__": ) ...