# database/repositories/__init__.py

from .ticket_repository import TicketRepository
from .incidente_repository import IncidenteRepository

__all__ = ["TicketRepository", "IncidenteRepository"]