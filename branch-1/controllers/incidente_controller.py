from typing import List, Optional, Dict, Any
from database.repositories.incidente_repository import IncidenteRepository
from models.incidente import Incidente


class IncidenteController:
    """Controlador de lógica de negocio para incidentes."""
    
    def __init__(self):
        self.repo = IncidenteRepository()
    
    def crear_incidente(
        self,
        descripcion: str,
        categoria: str,
        prioridad: str,
        ticket_id: int,
    ) -> Dict[str, Any]:
        """Crea un nuevo incidente asociado a un ticket."""
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
        
        incidente_guardado = self.repo.crear(incidente)
        
        return {
            "exito": True,
            "id": incidente_guardado.id,
            "mensaje": "Incidente creado exitosamente",
            "ticket_id": incidente_guardado.ticket_id,
        }
    
    def obtener_incidente(self, incidente_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene los detalles de un incidente."""
        incidente = self.repo.obtener_por_id(incidente_id)
        if incidente:
            return incidente.to_dict()
        return None
    
    def listar_incidentes(self) -> List[Dict[str, Any]]:
        """Lista todos los incidentes."""
        incidentes = self.repo.listar_todos()
        return [incidente.to_dict() for incidente in incidentes]
    
    def listar_incidentes_por_ticket(self, ticket_id: int) -> List[Dict[str, Any]]:
        """Lista todos los incidentes de un ticket específico."""
        incidentes = self.repo.listar_por_ticket(ticket_id)
        return [incidente.to_dict() for incidente in incidentes]
    
    def eliminar_incidente(self, incidente_id: int) -> Dict[str, Any]:
        """Elimina un incidente."""
        exito = self.repo.eliminar(incidente_id)
        if exito:
            return {
                "exito": True,
                "mensaje": f"Incidente {incidente_id} eliminado exitosamente",
            }
        return {
            "exito": False,
            "mensaje": f"No se encontró el incidente con ID {incidente_id}",
        }
    
    def filtrar_por_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        """Filtra incidentes por categoría."""
        incidentes = self.repo.filtrar_por_categoria(categoria)
        return [incidente.to_dict() for incidente in incidentes]
    
    def filtrar_por_prioridad(self, prioridad: str) -> List[Dict[str, Any]]:
        """Filtra incidentes por prioridad."""
        incidentes = self.repo.filtrar_por_prioridad(prioridad)
        return [incidente.to_dict() for incidente in incidentes]