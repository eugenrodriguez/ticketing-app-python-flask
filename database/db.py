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
    print("Base de datos inicializada con SQLAlchemy")


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