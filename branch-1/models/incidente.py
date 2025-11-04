from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Incidente(Base):
    __tablename__ = 'incidentes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False)
    prioridad = Column(String(50), nullable=False)
    
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    
    ticket = relationship("Ticket", back_populates="incidentes")
    
    def __init__(self, descripcion, categoria, prioridad, ticket_id):
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.ticket_id = ticket_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "ticket_id": self.ticket_id,
        }
    
    def __repr__(self):
        return f"<Incidente(id={self.id}, categoria='{self.categoria}', prioridad='{self.prioridad}')>"
