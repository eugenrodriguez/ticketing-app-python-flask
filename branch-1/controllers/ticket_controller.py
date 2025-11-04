from typing import Optional, Dict, Any, List
from database.repositories.ticket_repository import TicketRepository
from database.repositories.incidente_repository import IncidenteRepository
from models.ticket import Ticket
from models.incidente import Incidente


class TicketController:
    
    def __init__(self):
        self.ticket_repo = TicketRepository()
        self.incidente_repo = IncidenteRepository()
    
    def crear_ticket(
        self,
        cliente_id: int,
        servicio_id: int,
        equipo_id: int,
        empleado_id: int,
        incidentes_data: List[Dict[str, str]] = None,
    ) -> Dict[str, Any]:

        ticket = Ticket(
            cliente_id=cliente_id,
            servicio_id=servicio_id,
            equipo_id=equipo_id,
            empleado_id=empleado_id,
        )
        
        if incidentes_data:
            for inc_data in incidentes_data:
                incidente = Incidente(
                    descripcion=inc_data["descripcion"],
                    categoria=inc_data["categoria"],
                    prioridad=inc_data["prioridad"],
                    ticket_id=0 
                )
                ticket.incidentes.append(incidente)
        
        ticket_guardado = self.ticket_repo.crear(ticket)
        
        return {
            "exito": True,
            "id": ticket_guardado.id,
            "mensaje": "Ticket creado exitosamente",
            "estado": ticket_guardado.estado,
            "cantidad_incidentes": len(ticket_guardado.incidentes),
        }
    
    def obtener_ticket(self, ticket_id: int, incluir_incidentes: bool = True) -> Optional[Dict[str, Any]]:
        ticket = self.ticket_repo.obtener_por_id(ticket_id)
        if ticket:
            return ticket.to_dict(incluir_incidentes=incluir_incidentes)
        return None
    
    def listar_tickets(self, incluir_incidentes: bool = False) -> List[Dict[str, Any]]:
        tickets = self.ticket_repo.listar_todos()
        return [ticket.to_dict(incluir_incidentes=incluir_incidentes) for ticket in tickets]
    
    def cambiar_estado_ticket(self, ticket_id: int, nuevo_estado: str) -> Dict[str, Any]:
        estados_validos = ["Abierto", "En Progreso", "Cerrado", "Reabierto"]
        if nuevo_estado not in estados_validos:
            return {
                "exito": False,
                "mensaje": f"Estado inválido. Estados válidos: {', '.join(estados_validos)}",
            }
        
        exito = self.ticket_repo.actualizar_estado(ticket_id, nuevo_estado)
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
        exito = self.ticket_repo.cerrar_ticket(ticket_id)
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
        exito = self.ticket_repo.reabrir_ticket(ticket_id)
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
        tickets = self.ticket_repo.filtrar_por_estado(estado)
        return [ticket.to_dict() for ticket in tickets]
    
    def agregar_incidente_a_ticket(
        self, 
        ticket_id: int, 
        descripcion: str, 
        categoria: str, 
        prioridad: str
    ) -> Dict[str, Any]:

        categorias_validas = ["Hardware", "Software", "Red", "Otro"]
        prioridades_validas = ["Baja", "Media", "Alta", "Crítica"]
        
        if categoria not in categorias_validas:
            return {
                "exito": False,
                "mensaje": f"Categoría inválida. Válidas: {', '.join(categorias_validas)}",
            }
        
        if prioridad not in prioridades_validas:
            return {
                "exito": False,
                "mensaje": f"Prioridad inválida. Válidas: {', '.join(prioridades_validas)}",
            }
        
        incidente = Incidente(
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            ticket_id=ticket_id,
        )
        
        exito = self.ticket_repo.agregar_incidente(ticket_id, incidente)
        
        if exito:
            return {
                "exito": True,
                "id": incidente.id,
                "mensaje": f"Incidente agregado al ticket {ticket_id}",
            }
        return {
            "exito": False,
            "mensaje": f"No se encontró el ticket con ID {ticket_id}",
        }

