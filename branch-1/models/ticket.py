from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Ticket(Base):
    """Modelo de Ticket con SQLAlchemy - Relación 1:N con Incidentes."""
    __tablename__ = 'tickets'
    
    # Columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, nullable=False)
    servicio_id = Column(Integer, nullable=False)
    equipo_id = Column(Integer, nullable=False)
    empleado_id = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="Abierto")
    fecha_creacion = Column(String(50), nullable=False)
    fecha_cierre = Column(String(50), nullable=True)
    
    # Relación 1:N - Un ticket tiene muchos incidentes
    incidentes = relationship(
        "Incidente",
        back_populates="ticket",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    
    def __init__(self, cliente_id, servicio_id, equipo_id, empleado_id, estado="Abierto"):
        self.cliente_id = cliente_id
        self.servicio_id = servicio_id
        self.equipo_id = equipo_id
        self.empleado_id = empleado_id
        self.estado = estado
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_cierre = None
    
    def cerrar(self):
        """Cierra el ticket."""
        self.estado = "Cerrado"
        self.fecha_cierre = datetime.now().isoformat()
    
    def reabrir(self):
        """Reabre un ticket cerrado."""
        if self.estado == "Cerrado":
            self.estado = "Reabierto"
            self.fecha_cierre = None
    
    def to_dict(self, incluir_incidentes=False):
        """Convierte el ticket (objeto) a diccionario."""
        data = {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "servicio_id": self.servicio_id,
            "equipo_id": self.equipo_id,
            "empleado_id": self.empleado_id,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "fecha_cierre": self.fecha_cierre,
        }
        
        if incluir_incidentes:
            data["incidentes"] = [inc.to_dict() for inc in self.incidentes]
        else:
            data["cantidad_incidentes"] = len(self.incidentes)
        
        return data
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, estado='{self.estado}', incidentes={len(self.incidentes)})>"

