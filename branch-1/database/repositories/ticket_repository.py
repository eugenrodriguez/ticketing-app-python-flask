from typing import Optional, List
from sqlalchemy.orm import Session
from models.ticket import Ticket
from database.db import get_session


class TicketRepository:
    
    def __init__(self):
        self.session: Session = get_session()
    
    def crear(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket
    
    def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.session.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    def listar_todos(self) -> List[Ticket]:
        return self.session.query(Ticket).order_by(Ticket.id).all()
    
    def actualizar_estado(self, ticket_id: int, nuevo_estado: str) -> bool:
        ticket = self.obtener_por_id(ticket_id)
        if ticket:
            ticket.estado = nuevo_estado
            self.session.commit()
            return True
        return False
    
    def cerrar_ticket(self, ticket_id: int) -> bool:
        ticket = self.obtener_por_id(ticket_id)
        if ticket:
            ticket.cerrar()
            self.session.commit()
            return True
        return False
    
    def reabrir_ticket(self, ticket_id: int) -> bool:
        ticket = self.obtener_por_id(ticket_id)
        if ticket and ticket.estado == "Cerrado":
            ticket.reabrir()
            self.session.commit()
            return True
        return False
    
    def filtrar_por_estado(self, estado: str) -> List[Ticket]:
        return self.session.query(Ticket).filter(Ticket.estado == estado).all()
    
    def agregar_incidente(self, ticket_id: int, incidente) -> bool:
        ticket = self.obtener_por_id(ticket_id)
        if ticket:
            ticket.incidentes.append(incidente)
            self.session.commit()
            return True
        return False
