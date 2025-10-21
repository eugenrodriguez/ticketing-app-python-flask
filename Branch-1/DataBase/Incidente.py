from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from DataBase.db import base

class Incidente(base):
    __tablename__ = "incidente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ticket = Column(Integer, ForeignKey("ticket.id", ondelete="CASCADE" ), nullable=False)
    tipo = Column(String(200), nullable=False)
    descripcion = Column(TEXT, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_ticket": self.id_ticket,
            "tipo": self.tipo,
            "descripcion": self.descripcion
        }
    
    ticket = relationship("Ticket", back_populates="incidentes")