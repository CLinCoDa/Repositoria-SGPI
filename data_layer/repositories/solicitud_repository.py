from data_layer.database.database import db
from data_layer.models.solicitud import Solicitud, from_dict


class SolicitudRepository:

    @staticmethod
    def all():
        # devolver copia para evitar modificaciones externas accidentalmente
        return [from_dict(s) for s in db.solicitudes]

    @staticmethod
    def get(id: int):
        data = db.get_solicitud_by_id(id)
        return from_dict(data) if data else None

    @staticmethod
    def create(data: dict):
        # validar con modelo
        soli = from_dict(data)
        saved = db.add_solicitud(Solicitud.to_dict(soli))
        return from_dict(saved)

    @staticmethod
    def update(id: int, updates: dict):
        # combinar datos existentes + nuevos para validar
        existing = db.get_solicitud_by_id(id)
        if not existing:
            return None

        merged = {**existing, **updates}
        soli = from_dict(merged)  # validación

        updated = db.update_convocatoria(id, Solicitud.to_dict(soli))
        return from_dict(updated)

    @staticmethod
    def delete(id: int):
        return db.delete_solicitud(id)


