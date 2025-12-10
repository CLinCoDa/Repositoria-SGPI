from data_layer.database.database import db
from data_layer.models.convocatoria import Convocatoria, from_dict


class ConvocatoriaRepository:

    @staticmethod
    def all():
        # devolver copia para evitar modificaciones externas accidentalmente
        return [from_dict(c) for c in db.convocatorias]

    @staticmethod
    def get(id: int):
        data = db.get_convocatoria_by_id(id)
        return from_dict(data) if data else None

    @staticmethod
    def create(data: dict):
        # validar con modelo
        conv = from_dict(data)
        saved = db.add_convocatoria(Convocatoria.to_dict(conv))
        return from_dict(saved)

    @staticmethod
    def update(id: int, updates: dict):
        # combinar datos existentes + nuevos para validar
        existing = db.get_convocatoria_by_id(id)
        if not existing:
            return None

        merged = {**existing, **updates}
        conv = from_dict(merged)  # validación

        updated = db.update_convocatoria(id, Convocatoria.to_dict(conv))
        return from_dict(updated)

    @staticmethod
    def delete(id: int):
        return db.delete_convocatoria(id)


