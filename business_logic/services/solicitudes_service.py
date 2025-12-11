# business_logic/services/solicitudes_service.py

from data_layer.repositories.solicitud_repository import SolicitudRepository
from business_logic.services.convocatorias_service import listar_convocatorias

# Función auxiliar para la búsqueda de texto (case-insensitive)
def _search_text(solicitud, search_term):
    """Verifica si el término de búsqueda está en el código o el título."""
    search_term = search_term.lower()
    return (search_term in str(solicitud.codigo).lower() or
            search_term in str(solicitud.titulo).lower())


def listar_solicitudes(filters=None):

    # 1. Obtener todas las solicitudes inicialmente
    solics = SolicitudRepository.all()

    # 2. Si no hay filtros, devolver la lista completa
    if not filters:
        return solics

    # 3. Aplicar filtros secuencialmente (si el valor existe y no es 'all')

    # a) Filtrar por Estado
    estado_filter = filters.get("estado")
    if estado_filter and estado_filter != "":
        # Asegúrate de que ambos lados sean strings para la comparación segura
        solics = [s for s in solics if str(s.estado) == str(estado_filter)]

    # b) Filtrar por Convocatoria (convocatoria_id)
    convocatoria_filter = filters.get("convocatoria_id")
    # Es importante castear el ID a int si tu modelo usa int, o dejarlo como str si la DB lo usa así.
    # Asumimos que el valor del filtro viene como string del JS, pero el modelo puede ser int.
    if convocatoria_filter and convocatoria_filter != "":
        convocatoria_id_int = int(convocatoria_filter)
        solics = [s for s in solics if s.convocatoria_id == convocatoria_id_int]
        
    # c) Filtrar por Tipo de PI
    tipo_pi_filter = filters.get("tipo_pi") # Usamos tipo_pi para consistencia con Python
    if tipo_pi_filter and tipo_pi_filter != "":
        solics = [s for s in solics if str(s.tipo_pi) == str(tipo_pi_filter)]
        
    # d) Filtrar por Búsqueda (Search)
    search_filter = filters.get("search")
    if search_filter:
        solics = [s for s in solics if _search_text(s, search_filter)]

    return solics


def crear_solicitud(data):
    # Lógica de validación, asignación de user_id, y generación de código aquí
    # 
    return SolicitudRepository.create(data)

def eliminar_solicitud(id):
    # Lógica de seguridad (ej. solo el propietario o administrador puede eliminar)
    return SolicitudRepository.delete(id)

