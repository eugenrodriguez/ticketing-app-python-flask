from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.orm import relationship 
from DataBase.db import base

class Ticket(base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(255), nullable=False)
    operador = Column(String(255), nullable=False)
    equipo = Column(String(255), nullable=False)
    mensaje = Column(String(255), nullable=False)
    estado = Column(BOOLEAN, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "operador": self.operador,
            "equipo": self.equipo,
            "mensaje": self.mensaje,
            "estado": self.estado
        }
    
    incidentes = relationship("Incidente", back_populates="ticket", cascade="all, delete-orphan")