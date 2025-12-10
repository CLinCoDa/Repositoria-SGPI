# business_logic/managers/convocatoria_manager.py

from datetime import datetime
from data_layer.repositories.convocatoria_repository import get_all_convocatorias, add_convocatoria, delete_convocatoria

def filter_convocatorias(filters: dict):
    convocatorias = get_all_convocatorias()

    # Filtrado por año
    if 'year' in filters and filters['year'] != 'all':
        convocatorias = [c for c in convocatorias if str(c['year']) == str(filters['year'])]

    # Filtrado por tipo
    if 'type' in filters and filters['type'] != 'all':
        convocatorias = [c for c in convocatorias if c['type'] == filters['type']]

    # Filtrado por estado
    if 'status' in filters and filters['status'] != 'all':
        convocatorias = [c for c in convocatorias if c['status'] == filters['status']]

    # Filtrado por búsqueda de texto
    if 'search' in filters and filters['search']:
        search = filters['search'].lower()
        convocatorias = [
            c for c in convocatorias
            if search in (f"{c['year']} {c['trimester']}" if c['trimester'] else str(c['year'])).lower()
        ]

    # Ordenar por año descendente y trimestre
    trimester_order = {"T1": 1, "T2": 2, "T3": 3, "T4": 4, None: 5}
    convocatorias.sort(key=lambda c: (-c['year'], trimester_order.get(c['trimester'], 5)))

    return convocatorias

def create_convocatoria(data: dict):
    today = datetime.today().date()
    start = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

    # Determinar estado automático
    status = 'planificada'
    if start <= today <= end:
        status = 'registro'
    elif today > end:
        status = 'finalizada'

    convocatoria = {**data, 'status': status}
    add_convocatoria(convocatoria)
    return convocatoria

def remove_convocatoria(convocatoria_id: int):
    delete_convocatoria(convocatoria_id)
