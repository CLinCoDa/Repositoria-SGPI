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
            'email': 'admin@ug.edu.ec',
            'password_hash': hash_password('Admin123!'),
            'role': 'administrador',
            'full_name': 'Administrador del Sistema',
            'status': 'activo',
            'department': 'DIPI',
            'created_at': (now - timedelta(days=30)).isoformat(),
            'last_login': (now - timedelta(hours=2)).isoformat()
        },

        {
            'username': 'coordinador',
            'email': 'gestor.ingenieria@ug.edu.ec',
            'password_hash': hash_password('coordinador123'),
            'role': 'coordinador',
            'full_name': 'María González',
            'status': 'activo',
            'department': 'CATI-UG',
            'created_at': (now - timedelta(days=25)).isoformat(),
            'last_login': (now - timedelta(days=1)).isoformat()
        },

        {
            'username': 'gestor',
            'email': 'gestor.ing_software@ug.edu.ec',
            'password_hash': hash_password('Gestor123!'),
            'role': 'gestor',
            'full_name': 'María González',
            'status': 'activo',
            'department': 'Facultad de Ciencias Matematicas y Fisicas',
            'created_at': (now - timedelta(days=25)).isoformat(),
            'last_login': (now - timedelta(days=1)).isoformat()
        },
    ]

    # Generar docentes adicionales
    for i in range(1, 12): 
        base.append({
            'username': f'docente{i}',
            'email': f'docente{i}@ug.edu.ec',
            'password_hash': hash_password(f'Docente{i}123!'),
            'role': 'docente',
            'full_name': f'Docente Ejemplo {i}',
            'status': 'activo',
            'department': random.choice([
                'Facultad de Ciencias Matematicas y Fisicas',
                'Facultad de Ciencias Medicas',
                'Facultad de Ciencias Economicas',
                'Facultad de Ciencias Quimicas'
                'Facultad de Ciencias Ingenieria Industrial'
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
            'anio': current_year,
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
            'anio': current_year,
            'nombre': f'Convocatoria Extraordinaria - {current_year}',
            'descripcion': 'Convocatoria extraordinaria para proyectos especiales',
            'fecha_inicio': f'{current_year}-07-01',
            'fecha_fin': f'{current_year}-07-31',
            'estado': 'planificada',
            'publicada': False,
            'created_by': None
        })

    return convocatorias

def seed_solicitudes_docente1(docente_id):
    """
    Genera una lista predefinida de solicitudes específicas para un docente.
    """
    estados = ['borrador', 'enviada', 'en_revision', 'observada', 'aprobada', 'rechazada']

    solicitudes_docente1 = [
        # Solicitud 1: Patente - Enviada
        {
            'tipo': 'patente',
            'titulo': 'Sistema de filtración de agua por nanopartículas de plata',
            'descripcion': 'Desarrollo de un método innovador para purificar agua usando membranas con nanopartículas de plata embebidas.',
            'user_id': docente_id,
            'convocatoria_id': 1, # Ejemplo
            'estado': 'enviada',
            'fecha_registro': datetime(2025, 10, 15).isoformat()
        },
        # Solicitud 2: Derecho de Autor - Borrador
        {
            'tipo': 'derecho_autor',
            'titulo': 'Libro: Introducción a la robótica educativa',
            'descripcion': 'Manuscrito completo del libro de texto destinado a la enseñanza de robótica en nivel secundario.',
            'user_id': docente_id,
            'convocatoria_id': None,
            'estado': 'borrador',
            'fecha_registro': datetime(2025, 11, 20).isoformat()
        },
        # Solicitud 3: Modelo de Utilidad - Observada
        {
            'tipo': 'modelo_utilidad',
            'titulo': 'Adaptador ergonómico para microscopio de laboratorio',
            'descripcion': 'Mejora en la estructura de soporte de un microscopio estándar para reducir la fatiga visual y postural.',
            'user_id': docente_id,
            'convocatoria_id': 2, # Ejemplo
            'estado': 'observada',
            'fecha_registro': datetime(2025, 12, 1).isoformat()
        },
        # Solicitud 4: Marca - Aprobada
        {
            'tipo': 'marca',
            'titulo': 'Software "GeoMapp" para cartografía interactiva',
            'descripcion': 'Registro de la marca comercial para un nuevo software de código abierto desarrollado para visualización geográfica.',
            'user_id': docente_id,
            'convocatoria_id': None,
            'estado': 'aprobada',
            'fecha_registro': datetime(2024, 8, 5).isoformat()
        },
        # Solicitud 5: Diseño Industrial - Rechazada
        {
            'tipo': 'diseño_industrial',
            'titulo': 'Diseño estético de una luminaria de bajo consumo',
            'descripcion': 'Propuesta de la forma y apariencia ornamental de una lámpara LED modular.',
            'user_id': docente_id,
            'convocatoria_id': 3, # Ejemplo
            'estado': 'rechazada',
            'fecha_registro': datetime(2025, 9, 1).isoformat()
        },
        # Solicitud 6: Patente - En Revisión
        {
            'tipo': 'patente',
            'titulo': 'Proceso de síntesis de bioplástico a partir de residuos orgánicos',
            'descripcion': 'Método novedoso para la transformación de desechos alimenticios en material polimérico biodegradable.',
            'user_id': docente_id,
            'convocatoria_id': 1,
            'estado':  'revisada',
            'fecha_registro': datetime(2025, 12, 5).isoformat()
        }
    ]
    return solicitudes_docente1




def seed_solicitudes():
    solicitudes = []

    prefijos = {
        'patente': 'PT',
        'marca': 'MC',
        'derecho_autor': 'DA',
        'modelo_utilidad': 'MU',
        'diseño_industrial': 'DI'
    }

    tipos = list(prefijos.keys())
    estados = ['borrador', 'enviada', 'en_revision', 'observada', 'aprobada', 'rechazada']

    anio_actual = datetime.now().year

    for i in range(1, 10):
        tipo_seleccionado = random.choice(tipos)
        prefijo = prefijos[tipo_seleccionado]
        
        # Generar el número secuencial con relleno de ceros (ej: 001, 002, ..., 010)
        numero_secuencial = str(i).zfill(3) 
        
        # Construir el código final: Prefijo-Año-Secuencia (Ej: PT-2025-001)
        codigo_generado = f'{prefijo}-{anio_actual}-{numero_secuencial}'

        solicitudes.append({
            'codigo': codigo_generado,
            'tipo_pi': tipo_seleccionado,
            'titulo': f'Solicitud ejemplo {i}',
            'descripcion': 'Descripción de ejemplo',
            'user_id': None,           # se asignará cuando se inserte (o puedes mapear con usuarios seed)
            'convocatoria_id': None,
            'estado': random.choice(estados),
            'fecha_envio': datetime.now().isoformat()
        })

    return solicitudes