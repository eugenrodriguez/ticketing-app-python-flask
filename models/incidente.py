from dataclasses import dataclass


@dataclass
class Incidente:
    """Representa un incidente registrado en el sistema."""
    id: int
    descripcion: str
    categoria: str
    prioridad: str
    
    def to_dict(self) -> dict:
        """Convierte el incidente a diccionario para serialización."""
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
        }