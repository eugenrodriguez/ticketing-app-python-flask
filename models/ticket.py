from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Ticket:
    """Representa un ticket de servicio técnico."""
    id: int
    cliente_id: int
    servicio_id: int
    equipo_id: int
    empleado_id: int
    incidente_id: int
    estado: str = "Abierto"
    fecha_creacion: Optional[str] = None
    fecha_cierre: Optional[str] = None
    
    def __post_init__(self):
        """Inicializa la fecha de creación si no se proporciona."""
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now().isoformat()
    
    def cerrar(self) -> None:
        """Cierra el ticket."""
        self.estado = "Cerrado"
        self.fecha_cierre = datetime.now().isoformat()
    
    def reabrir(self) -> None:
        """Reabre un ticket cerrado."""
        if self.estado == "Cerrado":
            self.estado = "Reabierto"
            self.fecha_cierre = None
    
    def to_dict(self) -> dict:
        """Convierte el ticket a diccionario para serialización."""
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "servicio_id": self.servicio_id,
            "equipo_id": self.equipo_id,
            "empleado_id": self.empleado_id,
            "incidente_id": self.incidente_id,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "fecha_cierre": self.fecha_cierre,
        }