from DataBase.db import Sesion
from DataBase.Ticket import Ticket

class TicketRepository:
    def __init__(self):
        self.sesion = Sesion()
        
    def crear(self, cliente, operador, equipo, mensaje, estado):
        ticket = Ticket(cliente=cliente, operador=operador, equipo=equipo, mensaje=mensaje, estado=estado)
        self.sesion.add(ticket)
        self.sesion.commit()
        
    def listar(self):
        return self.sesion.query(Ticket).all()
    
    def buscar(self, id):
        return self.sesion.get(Ticket, id)
    
    def borrar(self, id):
        ticket = self.sesion.get(Ticket, id)
        
        if ticket:
            self.sesion.delete(ticket)
            self.sesion.commit()
            return True
            
        else:
            return False
        
    def modificar(self, id, cliente=None, operador=None, equipo=None, mensaje=None, estado=None):
        ticket = self.sesion.get(Ticket, id)
        if not ticket:
            return False
        
        if cliente is not None:
            ticket.cliente = cliente
        if operador is not None:
            ticket.operador = operador
        if equipo is not None:
            ticket.equipo = equipo
        if mensaje is not None:
            ticket.mensaje = mensaje 
        if estado is not None:
            ticket.estado = estado

        self.sesion.commit()
        return True