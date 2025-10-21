from typing import Optional, List
from sqlalchemy.orm import Session
from models.incidente import Incidente
from database.db import get_session


class IncidenteRepository:
    """Repositorio para operaciones CRUD de Incidentes con SQLAlchemy."""
    
    def __init__(self):
        self.session: Session = get_session()
    
    def crear(self, incidente: Incidente) -> Incidente:
        """Crea un nuevo incidente en la base de datos."""
        self.session.add(incidente)
        self.session.commit()
        self.session.refresh(incidente)
        return incidente
    
    def obtener_por_id(self, incidente_id: int) -> Optional[Incidente]:
        """Obtiene un incidente por su ID."""
        return self.session.query(Incidente).filter(Incidente.id == incidente_id).first()
    
    def listar_todos(self) -> List[Incidente]:
        """Lista todos los incidentes."""
        return self.session.query(Incidente).order_by(Incidente.id).all()
    
    def listar_por_ticket(self, ticket_id: int) -> List[Incidente]:
        """Lista todos los incidentes de un ticket específico."""
        return self.session.query(Incidente).filter(Incidente.ticket_id == ticket_id).all()
    
    def eliminar(self, incidente_id: int) -> bool:
        """Elimina un incidente por su ID."""
        incidente = self.obtener_por_id(incidente_id)
        if incidente:
            self.session.delete(incidente)
            self.session.commit()
            return True
        return False
    
    def filtrar_por_categoria(self, categoria: str) -> List[Incidente]:
        """Filtra incidentes por categoría."""
        return self.session.query(Incidente).filter(Incidente.categoria == categoria).all()
    
    def filtrar_por_prioridad(self, prioridad: str) -> List[Incidente]:
        """Filtra incidentes por prioridad."""
        return self.session.query(Incidente).filter(Incidente.prioridad == prioridad).all()
    
    def actualizar(self, incidente: Incidente) -> Incidente:
        """Actualiza un incidente existente."""
        self.session.commit()
        self.session.refresh(incidente)
        return incidente