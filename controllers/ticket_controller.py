from typing import Optional, Dict, Any, List
from database.db import get_connection


class TicketController:
    def __init__(self, db_path: str = "app.db"):
        self.conn = get_connection(db_path)

    def _ensure_cliente(self, nombre: str, email: str, telefono: str, direccion: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM clientes WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?, ?, ?, ?)",
            (nombre, email, telefono, direccion),
        )
        self.conn.commit()
        return cursor.lastrowid

    def _ensure_empleado(self, nombre: str, categoria: str, rol: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM empleados WHERE nombre = ? AND categoria = ? AND rol = ?",
            (nombre, categoria, rol),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(
            "INSERT INTO empleados (nombre, categoria, rol) VALUES (?, ?, ?)",
            (nombre, categoria, rol),
        )
        self.conn.commit()
        return cursor.lastrowid

    def _ensure_equipo(self, descripcion: str, categoria: str, marca: str, modelo: str, nro_serie: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM equipos WHERE nro_serie = ?",
            (nro_serie,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(
            """
            INSERT INTO equipos (descripcion, categoria, marca, modelo, nro_serie)
            VALUES (?, ?, ?, ?, ?)
            """,
            (descripcion, categoria, marca, modelo, nro_serie),
        )
        self.conn.commit()
        return cursor.lastrowid

    def _ensure_servicio(self, nombre: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM servicios WHERE nombre = ?", (nombre,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute("INSERT INTO servicios (nombre) VALUES (?)", (nombre,))
        self.conn.commit()
        return cursor.lastrowid

    def crear_ticket(
        self,
        cliente: Dict[str, Any],
        servicio: Dict[str, Any],
        equipo: Dict[str, Any],
        empleado: Dict[str, Any],
        incidente: Dict[str, Any],
        fecha_creacion: Optional[str] = None,
    ) -> int:
        # Ensure or create related entities
        cliente_id = self._ensure_cliente(
            cliente["nombre"], cliente["email"], cliente["telefono"], cliente["direccion"]
        )
        servicio_id = self._ensure_servicio(servicio["nombre"])  # minimal schema
        equipo_id = self._ensure_equipo(
            equipo["descripcion"], equipo["categoria"], equipo["marca"], equipo["modelo"], equipo["nro_serie"],
        )
        empleado_id = self._ensure_empleado(
            empleado["nombre"], empleado["categoria"], empleado["rol"],
        )

        # Incidente must exist (created from IncidenteController or here)
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM incidentes WHERE id = ?",
            (incidente["id"],),
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO incidentes (descripcion, categoria, prioridad) VALUES (?, ?, ?)",
                (incidente["descripcion"], incidente["categoria"], incidente["prioridad"]),
            )
            self.conn.commit()
            incidente_id = cursor.lastrowid
        else:
            incidente_id = incidente["id"]

        # Create ticket
        cursor.execute(
            """
            INSERT INTO tickets (
                cliente_id, servicio_id, equipo_id, empleado_id, incidente_id, estado, fecha_creacion, fecha_cierre
            ) VALUES (?, ?, ?, ?, ?, 'Abierto', COALESCE(?, datetime('now')), NULL)
            """,
            (cliente_id, servicio_id, equipo_id, empleado_id, incidente_id, fecha_creacion),
        )
        self.conn.commit()
        return cursor.lastrowid

    def reabrir_ticket(self, ticket_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT estado FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        estado_actual = row[0]
        if estado_actual == "Cerrado":
            cursor.execute(
                "UPDATE tickets SET estado = 'Reabierto', fecha_cierre = NULL WHERE id = ?",
                (ticket_id,),
            )
            self.conn.commit()
            return True
        return False

    def cerrar_ticket(self, ticket_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tickets SET estado = 'Cerrado', fecha_cierre = datetime('now') WHERE id = ?", (ticket_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def agregar_trabajo(self, ticket_id: int, autor: str, contenido: str, fecha: Optional[str] = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,))
        if cursor.fetchone() is None:
            raise ValueError("Ticket no encontrado")
        cursor.execute(
            "INSERT INTO trabajos (ticket_id, autor, contenido, fecha) VALUES (?, ?, ?, COALESCE(?, datetime('now')))",
            (ticket_id, autor, contenido, fecha),
        )
        self.conn.commit()
        return cursor.lastrowid

    def ver_historial(self, ticket_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, autor, contenido, fecha FROM trabajos WHERE ticket_id = ? ORDER BY id ASC",
            (ticket_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def obtener_ticket(self, ticket_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.nombre AS cliente_nombre, s.nombre AS servicio_nombre,
                   e.nombre AS empleado_nombre, i.descripcion AS incidente_descripcion
            FROM tickets t
            JOIN clientes c ON t.cliente_id = c.id
            JOIN servicios s ON t.servicio_id = s.id
            JOIN empleados e ON t.empleado_id = e.id
            JOIN incidentes i ON t.incidente_id = i.id
            WHERE t.id = ?
            """,
            (ticket_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass


