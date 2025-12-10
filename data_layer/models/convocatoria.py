# models/convocatorias.py

from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Optional

# -----------------------------
#  CONSTANTES
# -----------------------------
TIPOS_CONVOCATORIA = ["normal", "extraordinaria"]
ESTADOS_CONVOCATORIA = ["planificada", "registro", "finalizada"]


# -----------------------------
#  VALIDADORES
# -----------------------------
def validar_tipo(tipo: str):
    if tipo not in TIPOS_CONVOCATORIA:
        raise ValueError(f"Tipo de convocatoria inválido: {tipo}")


def validar_fechas(fecha_inicio: str, fecha_fin: str):
    try:
        f1 = datetime.fromisoformat(fecha_inicio)
        f2 = datetime.fromisoformat(fecha_fin)
    except Exception:
        raise ValueError("Las fechas deben estar en formato ISO (YYYY-MM-DD).")

    if f1 > f2:
        raise ValueError("fecha_inicio no puede ser mayor que fecha_fin.")


def calcular_estado(fecha_inicio: str, fecha_fin: str) -> str:
    today = date.today()
    f1 = datetime.fromisoformat(fecha_inicio).date()
    f2 = datetime.fromisoformat(fecha_fin).date()

    if today < f1:
        return "planificada"
    elif f1 <= today <= f2:
        return "registro"
    else:
        return "finalizada"


# -----------------------------
#  MODELO
# -----------------------------
@dataclass
class Convocatoria:
    tipo: str
    anio: int
    nombre: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: str
    trimestre: Optional[int] = None
    estado: Optional[str] = None
    publicada: bool = False
    created_by: Optional[int] = None

    id: Optional[int] = field(default=None)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        # validación de tipo
        validar_tipo(self.tipo)

        # validación de fechas
        validar_fechas(self.fecha_inicio, self.fecha_fin)

        # autogenerar estado si no viene
        if self.estado is None:
            self.estado = calcular_estado(self.fecha_inicio, self.fecha_fin)

        # timestamps por defecto
        now = datetime.now().isoformat()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
    
    def to_dict(self):
        return asdict(self)


def from_dict(data: dict) -> Convocatoria:
    return Convocatoria(**data)



