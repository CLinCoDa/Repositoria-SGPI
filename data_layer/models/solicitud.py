from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Optional

@dataclass
class Solicitud:
    """
    Representa una solicitud de registro de Propiedad Intelectual.
    """
    
    # Campos que deben ser proporcionados al crear la instancia
    tipo_pi: str
    titulo: str
    user_id: int 
    
    # --- Atributos Opcionales de Contenido y Enlace ---
    
    descripcion: Optional[str] = None
    convocatoria_id: Optional[int] = None
    observaciones: Optional[str] = None # Notas del revisor
    
    # --- Atributos de Trazabilidad y Estado (Definidos por el sistema) ---
    
    # El estado inicial debe ser 'borrador' si no se especifica
    estado: Optional[str] = None 
    
    # Fecha de envío formal (se establece cuando se cambia el estado a 'enviada')
    fecha_envio: Optional[str] = None 
    
    # Revisor que está a cargo
    revisor_id: Optional[int] = None 

    # --- Campos de BBDD y Timestamps ---
    
    id: Optional[int] = field(default=None) # Primary Key (PK)
    codigo: Optional[str] = field(default=None) # Código generado (Ej: PT-2025-001)
    
    created_at: Optional[str] = field(default=None)
    updated_at: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    
    def __post_init__(self):
        """Lógica de inicialización y validación después de __init__."""
        
        # 1. Validación de tipo PI (Asumiendo que tienes una función)
        # validar_tipo_solicitud(self.tipo_pi) 
        
        now = datetime.now().isoformat()
        
        # 2. Timestamps por defecto
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
        
        # 3. Autogenerar estado inicial
        if self.estado is None:
            # Si tiene fecha_envio, se podría inferir 'enviada', si no, es 'borrador'
            if self.fecha_envio:
                self.estado = 'enviada'
            else:
                self.estado = 'borrador'

        # 4. Generación de Código (Normalmente manejado por el servicio/ORM)
        # if self.codigo is None:
        #    self.codigo = self._generar_codigo_inicial()

    def to_dict(self) -> dict:
        """Convierte la instancia de dataclass a un diccionario."""
        return asdict(self)

    # --- Método Auxiliar para la generación de código (Placeholder) ---
    # def _generar_codigo_inicial(self):
    #     # Lógica para generar PT-AÑO-SECUENCIA
    #     prefijos = {'patente': 'PT', 'marca': 'MC', ...}
    #     prefijo = prefijos.get(self.tipo_pi, 'XX')
    #     return f"{prefijo}-{datetime.now().year}-TEMP"

def from_dict(data: dict) -> Solicitud:
    """Crea una instancia de Solicitud a partir de un diccionario."""
    # Filtra las claves no esperadas si es necesario antes de la desestructuración:
    return Solicitud(**data)