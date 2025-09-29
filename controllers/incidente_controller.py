from typing import List, Optional, Dict, Any
from database.db import get_connection


class IncidenteController:
    def __init__(self, db_path: str = "app.db"):
        self.conn = get_connection(db_path)

    def listar(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, descripcion, categoria, prioridad FROM incidentes ORDER BY id ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def crear(self, descripcion: str, categoria: str, prioridad: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO incidentes (descripcion, categoria, prioridad) VALUES (?, ?, ?)",
            (descripcion, categoria, prioridad),
        )
        self.conn.commit()
        return cursor.lastrowid

    def obtener(self, incidente_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, descripcion, categoria, prioridad FROM incidentes WHERE id = ?",
            (incidente_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def eliminar(self, incidente_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM incidentes WHERE id = ?", (incidente_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        # La conexión es compartida y la gestiona database/db.py
        return None


