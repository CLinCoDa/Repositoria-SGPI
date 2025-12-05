# data_layer/seed_data.py
"""
Datos de ejemplo para desarrollo y pruebas
No incluyen 'id' para permitir autoincremento del Database
"""

from datetime import datetime, timedelta
import random
from business_logic.utils.password_utils import hash_password

def seed_users():
    now = datetime.now()
    base = [
        {
            'username': 'admin',
            'email': 'admin@sgpi.edu',
            'password_hash': hash_password('Admin123!'),
            'role': 'administrador',
            'full_name': 'Administrador del Sistema',
            'status': 'activo',
            'department': 'dipi',
            'created_at': (now - timedelta(days=30)).isoformat(),
            'last_login': (now - timedelta(hours=2)).isoformat()
        },
        {
            'username': 'gestor_ingenieria',
            'email': 'gestor.ingenieria@sgpi.edu',
            'password_hash': hash_password('Gestor123!'),
            'role': 'gestor',
            'full_name': 'María González',
            'status': 'activo',
            'department': 'facultad_ingenieria',
            'created_at': (now - timedelta(days=25)).isoformat(),
            'last_login': (now - timedelta(days=1)).isoformat()
        },
    ]

    # Generar docentes adicionales
    for i in range(1, 12):  # 11 docentes => total usuarios ~13
        base.append({
            'username': f'docente{i}',
            'email': f'docente{i}@sgpi.edu',
            'password_hash': hash_password(f'Docente{i}123!'),
            'role': 'docente',
            'full_name': f'Docente Ejemplo {i}',
            'status': 'activo',
            'department': random.choice([
                'facultad_ingenieria',
                'facultad_salud',
                'facultad_sociales',
                'facultad_ciencias'
            ]),
            'created_at': (now - timedelta(days=random.randint(1, 20))).isoformat(),
            'last_login': (now - timedelta(days=random.randint(0, 10))).isoformat() if random.random() > 0.3 else None
        })

    return base

def seed_convocatorias():
    convocatorias = []
    current_year = datetime.now().year
    for i in range(1, 5):
        convocatorias.append({
            'tipo': 'normal',
            'ano': current_year,
            'trimestre': i,
            'nombre': f'Convocatoria T{i} - {current_year}',
            'descripcion': f'Convocatoria del {i}° trimestre del año {current_year}',
            'fecha_inicio': f'{current_year}-{(i-1)*3+1:02d}-01',
            'fecha_fin': f'{current_year}-{i*3:02d}-28',
            'estado': 'finalizada' if i < 4 else 'registro',
            'publicada': True,
            'created_by': None
        })

    convocatorias.append({
        'tipo': 'extraordinaria',
        'ano': current_year,
        'nombre': f'Convocatoria Extraordinaria - {current_year}',
        'descripcion': 'Convocatoria extraordinaria para proyectos especiales',
        'fecha_inicio': f'{current_year}-07-01',
        'fecha_fin': f'{current_year}-07-31',
        'estado': 'planificada',
        'publicada': False,
        'created_by': None
    })

    return convocatorias

def seed_solicitudes():
    solicitudes = []
    tipos = ['patente', 'marca', 'derecho_autor', 'modelo_utilidad', 'diseño_industrial']
    estados = ['borrador', 'enviada', 'en_revision', 'observada', 'aprobada', 'rechazada']
    for i in range(1, 21):
        solicitudes.append({
            'tipo': random.choice(tipos),
            'titulo': f'Solicitud ejemplo {i}',
            'descripcion': 'Descripción de ejemplo',
            'user_id': None,           # se asignará cuando se inserte (o puedes mapear con usuarios seed)
            'convocatoria_id': None,
            'estado': random.choice(estados),
            'fecha_registro': datetime.now().isoformat()
        })
    return solicitudes
