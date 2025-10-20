from typing import Optional, List, Dict, Any
from database.db import get_connection
from models.ticket import Ticket


class TicketRepository:
    """Encapsula la lógica de acceso a datos para tickets."""
    
    def __init__(self, db_path: str = "app.db"):
        self.conn = get_connection(db_path)
    
    def crear(self, ticket: Ticket) -> int:
        """Inserta un ticket en la base de datos."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO tickets (
                cliente_id, servicio_id, equipo_id, empleado_id, 
                incidente_id, estado, fecha_creacion, fecha_cierre
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.cliente_id,
                ticket.servicio_id,
                ticket.equipo_id,
                ticket.empleado_id,
                ticket.incidente_id,
                ticket.estado,
                ticket.fecha_creacion,
                ticket.fecha_cierre,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
        """Obtiene un ticket por su ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, cliente_id, servicio_id, equipo_id, empleado_id,
                   incidente_id, estado, fecha_creacion, fecha_cierre
            FROM tickets WHERE id = ?
            """,
            (ticket_id,),
        )
        row = cursor.fetchone()
        if row:
            return Ticket(
                id=row[0],
                cliente_id=row[1],
                servicio_id=row[2],
                equipo_id=row[3],
                empleado_id=row[4],
                incidente_id=row[5],
                estado=row[6],
                fecha_creacion=row[7],
                fecha_cierre=row[8],
            )
        return None
    
    def listar_todos(self) -> List[Ticket]:
        """Obtiene todos los tickets."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, cliente_id, servicio_id, equipo_id, empleado_id,
                   incidente_id, estado, fecha_creacion, fecha_cierre
            FROM tickets ORDER BY id ASC
            """
        )
        rows = cursor.fetchall()
        return [
            Ticket(
                id=row[0],
                cliente_id=row[1],
                servicio_id=row[2],
                equipo_id=row[3],
                empleado_id=row[4],
                incidente_id=row[5],
                estado=row[6],
                fecha_creacion=row[7],
                fecha_cierre=row[8],
            )
            for row in rows
        ]
    
    def actualizar_estado(self, ticket_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de un ticket."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tickets SET estado = ? WHERE id = ?",
            (nuevo_estado, ticket_id),
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def cerrar_ticket(self, ticket_id: int) -> bool:
        """Cierra un ticket registrando la fecha de cierre."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE tickets 
            SET estado = 'Cerrado', fecha_cierre = datetime('now')
            WHERE id = ?
            """,
            (ticket_id,),
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def reabrir_ticket(self, ticket_id: int) -> bool:
        """Reabre un ticket cerrado."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT estado FROM tickets WHERE id = ?",
            (ticket_id,),
        )
        row = cursor.fetchone()
        if row and row[0] == "Cerrado":
            cursor.execute(
                """
                UPDATE tickets 
                SET estado = 'Reabierto', fecha_cierre = NULL
                WHERE id = ?
                """,
                (ticket_id,),
            )
            self.conn.commit()
            return True
        return False
    
    def filtrar_por_estado(self, estado: str) -> List[Ticket]:
        """Filtra tickets por estado."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, cliente_id, servicio_id, equipo_id, empleado_id,
                   incidente_id, estado, fecha_creacion, fecha_cierre
            FROM tickets WHERE estado = ?
            """,
            (estado,),
        )
        rows = cursor.fetchall()
        return [
            Ticket(
                id=row[0],
                cliente_id=row[1],
                servicio_id=row[2],
                equipo_id=row[3],
                empleado_id=row[4],
                incidente_id=row[5],
                estado=row[6],
                fecha_creacion=row[7],
                fecha_cierre=row[8],
            )
            for row in rows
        ]