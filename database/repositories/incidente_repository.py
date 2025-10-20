from typing import Optional, List
from database.db import get_connection
from models.incidente import Incidente


class IncidenteRepository:
    """Encapsula la lógica de acceso a datos para incidentes."""
    
    def __init__(self, db_path: str = "app.db"):
        self.conn = get_connection(db_path)
    
    def crear(self, incidente: Incidente) -> int:
        """Inserta un incidente en la base de datos."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO incidentes (descripcion, categoria, prioridad)
            VALUES (?, ?, ?)
            """,
            (incidente.descripcion, incidente.categoria, incidente.prioridad),
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def obtener_por_id(self, incidente_id: int) -> Optional[Incidente]:
        """Obtiene un incidente por su ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, descripcion, categoria, prioridad
            FROM incidentes WHERE id = ?
            """,
            (incidente_id,),
        )
        row = cursor.fetchone()
        if row:
            return Incidente(
                id=row[0],
                descripcion=row[1],
                categoria=row[2],
                prioridad=row[3],
            )
        return None
    
    def listar_todos(self) -> List[Incidente]:
        """Obtiene todos los incidentes."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, descripcion, categoria, prioridad FROM incidentes ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        return [
            Incidente(
                id=row[0],
                descripcion=row[1],
                categoria=row[2],
                prioridad=row[3],
            )
            for row in rows
        ]
    
    def eliminar(self, incidente_id: int) -> bool:
        """Elimina un incidente por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM incidentes WHERE id = ?", (incidente_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def filtrar_por_categoria(self, categoria: str) -> List[Incidente]:
        """Filtra incidentes por categoría."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, descripcion, categoria, prioridad
            FROM incidentes WHERE categoria = ?
            """,
            (categoria,),
        )
        rows = cursor.fetchall()
        return [
            Incidente(
                id=row[0],
                descripcion=row[1],
                categoria=row[2],
                prioridad=row[3],
            )
            for row in rows
        ]
    
    def filtrar_por_prioridad(self, prioridad: str) -> List[Incidente]:
        """Filtra incidentes por prioridad."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, descripcion, categoria, prioridad
            FROM incidentes WHERE prioridad = ?
            """,
            (prioridad,),
        )
        rows = cursor.fetchall()
        return [
            Incidente(
                id=row[0],
                descripcion=row[1],
                categoria=row[2],
                prioridad=row[3],
            )
            for row in rows
        ]