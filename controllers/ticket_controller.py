from typing import Optional, Dict, Any, List
from database.repositories.ticket_repository import TicketRepository
from models.ticket import Ticket


class TicketController:
    """Controlador de lógica de negocio para tickets."""
    
    def __init__(self, db_path: str = "app.db"):
        self.repo = TicketRepository(db_path)
    
    def crear_ticket(
        self,
        cliente_id: int,
        servicio_id: int,
        equipo_id: int,
        empleado_id: int,
        incidente_id: int,
    ) -> Dict[str, Any]:
        """Crea un nuevo ticket."""
        ticket = Ticket(
            id=0,  # Se asignará en BD
            cliente_id=cliente_id,
            servicio_id=servicio_id,
            equipo_id=equipo_id,
            empleado_id=empleado_id,
            incidente_id=incidente_id,
        )
        ticket_id = self.repo.crear(ticket)
        return {
            "id": ticket_id,
            "mensaje": "Ticket creado exitosamente",
            "estado": "Abierto",
        }
    
    def obtener_ticket(self, ticket_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene los detalles de un ticket."""
        ticket = self.repo.obtener_por_id(ticket_id)
        if ticket:
            return ticket.to_dict()
        return None
    
    def listar_tickets(self) -> List[Dict[str, Any]]:
        """Lista todos los tickets."""
        tickets = self.repo.listar_todos()
        return [ticket.to_dict() for ticket in tickets]
    
    def cambiar_estado_ticket(self, ticket_id: int, nuevo_estado: str) -> Dict[str, Any]:
        """Cambia el estado de un ticket."""
        estados_validos = ["Abierto", "En Progreso", "Cerrado", "Reabierto"]
        if nuevo_estado not in estados_validos:
            return {
                "exito": False,
                "mensaje": f"Estado inválido. Estados válidos: {', '.join(estados_validos)}",
            }
        
        exito = self.repo.actualizar_estado(ticket_id, nuevo_estado)
        if exito:
            return {
                "exito": True,
                "mensaje": f"Ticket {ticket_id} actualizado a {nuevo_estado}",
            }
        return {
            "exito": False,
            "mensaje": f"No se encontró el ticket con ID {ticket_id}",
        }
    
    def cerrar_ticket(self, ticket_id: int) -> Dict[str, Any]:
        """Cierra un ticket."""
        exito = self.repo.cerrar_ticket(ticket_id)
        if exito:
            return {
                "exito": True,
                "mensaje": f"Ticket {ticket_id} cerrado exitosamente",
            }
        return {
            "exito": False,
            "mensaje": f"No se encontró el ticket con ID {ticket_id}",
        }
    
    def reabrir_ticket(self, ticket_id: int) -> Dict[str, Any]:
        """Reabre un ticket cerrado."""
        exito = self.repo.reabrir_ticket(ticket_id)
        if exito:
            return {
                "exito": True,
                "mensaje": f"Ticket {ticket_id} reabierto exitosamente",
            }
        return {
            "exito": False,
            "mensaje": f"No se pudo reabrir el ticket {ticket_id}. Verifique que esté cerrado",
        }
    
    def filtrar_por_estado(self, estado: str) -> List[Dict[str, Any]]:
        """Filtra tickets por estado."""
        tickets = self.repo.filtrar_por_estado(estado)
        return [ticket.to_dict() for ticket in tickets]