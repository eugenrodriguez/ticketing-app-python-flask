import sqlite3
import threading
from typing import Optional


_connection: Optional[sqlite3.Connection] = None
_lock = threading.Lock()


def get_connection(db_path: str = "app.db") -> sqlite3.Connection:
    global _connection
    if _connection is not None:
        return _connection
    with _lock:
        if _connection is None:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            _initialize_schema(conn)
            _set_connection(conn)
    return _connection  # type: ignore[return-value]


def _set_connection(conn: sqlite3.Connection) -> None:
    global _connection
    _connection = conn


def _initialize_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    # Entidades principales
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            nro_serie TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            prioridad TEXT NOT NULL
        )
        """
    )

    # Tickets y trabajos (historial)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            equipo_id INTEGER NOT NULL,
            empleado_id INTEGER NOT NULL,
            incidente_id INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Abierto',
            fecha_creacion TEXT NOT NULL,
            fecha_cierre TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (servicio_id) REFERENCES servicios(id),
            FOREIGN KEY (equipo_id) REFERENCES equipos(id),
            FOREIGN KEY (empleado_id) REFERENCES empleados(id),
            FOREIGN KEY (incidente_id) REFERENCES incidentes(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trabajos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            autor TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
        """
    )

    conn.commit()


def close_connection() -> None:
    global _connection
    if _connection is not None:
        try:
            _connection.close()
        finally:
            _connection = None


