"""
Configuración de la base de datos con SQLAlchemy.
Gestiona la conexión, sesiones y creación de tablas.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from typing import Optional

# Variables globales para engine y session
_engine = None
_session_factory = None
_scoped_session = None


def init_db(db_path: str = "app.db") -> None:
    """Inicializa la base de datos y crea las tablas si no existen."""
    global _engine, _session_factory, _scoped_session
    
    if _engine is not None:
        return  # Ya está inicializada
    
    # Crear engine de SQLAlchemy
    database_url = f"sqlite:///{db_path}"
    _engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Para SQLite en Flask
        echo=False,  # True para debug SQL
    )
    
    # Crear session factory
    _session_factory = sessionmaker(bind=_engine)
    _scoped_session = scoped_session(_session_factory)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from models.ticket import Ticket
    from models.incidente import Incidente
    
    # Crear todas las tablas
    Base.metadata.create_all(_engine)
    
    # Crear tablas hardcodeadas (clientes, empleados, etc.)
    _crear_tablas_auxiliares()
    
    print("Base de datos inicializada con SQLAlchemy")


def _crear_tablas_auxiliares() -> None:
    """Crea tablas auxiliares que no son modelos SQLAlchemy (hardcodeadas)."""
    from sqlalchemy import text
    
    with _engine.connect() as conn:
        # Tabla clientes
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL
            )
        """))
        
        # Tabla empleados
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """))
        
        # Tabla equipos
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS equipos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                categoria TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                nro_serie TEXT NOT NULL
            )
        """))
        
        # Tabla servicios
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        """))
        
        # Tabla trabajos (mensajes)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS trabajos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                autor TEXT NOT NULL,
                contenido TEXT NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            )
        """))
        
        conn.commit()


def get_session():
    """Obtiene una sesión de SQLAlchemy."""
    if _scoped_session is None:
        init_db()
    return _scoped_session()


def close_session() -> None:
    """Cierra la sesión actual."""
    if _scoped_session is not None:
        _scoped_session.remove()


def close_db() -> None:
    """Cierra la conexión a la base de datos."""
    global _engine, _session_factory, _scoped_session
    
    if _scoped_session is not None:
        _scoped_session.remove()
        _scoped_session = None
    
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _session_factory = None
    
    print(" Base de datos cerrada")