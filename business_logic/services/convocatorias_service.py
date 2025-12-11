# business_logic/services/convocatorias_service.py

from data_layer.repositories.convocatoria_repository import ConvocatoriaRepository



def listar_convocatorias(filters=None):
    convs = ConvocatoriaRepository.all()

    if filters:
        year = filters.get("year")
        type_ = filters.get("type")
        status = filters.get("status")
        search = filters.get("search")

        if year:
            convs = [c for c in convs if str(c.anio) == str(year)]

        if type_ and type_ != "all":
            convs = [c for c in convs if c.tipo == type_]

        if status and status != "all":
            convs = [c for c in convs if c.estado == status]

        if search:
            txt = search.lower()
            convs = [
                c for c in convs
                if txt in c.descripcion.lower() or txt in c.tipo.lower()
            ]

    return convs


def crear_convocatoria(data: dict):

    return ConvocatoriaRepository.create(data)

def editar_convocatoria(id: int,data: dict):
    return ConvocatoriaRepository.update(id,data)

def eliminar_convocatoria(id):
    return ConvocatoriaRepository.delete(id)

