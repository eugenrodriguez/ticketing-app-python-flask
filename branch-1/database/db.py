from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from typing import Optional

_engine = None
_session_factory = None
_scoped_session = None


def init_db(db_path: str = "app.db") -> None:
    global _engine, _session_factory, _scoped_session
    
    if _engine is not None:
        return  
    
    database_url = f"sqlite:///{db_path}"
    _engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}, 
        echo=False,  
    )
    
    _session_factory = sessionmaker(bind=_engine)
    _scoped_session = scoped_session(_session_factory)
    
    from models.ticket import Ticket
    from models.incidente import Incidente
    
    Base.metadata.create_all(_engine)
    
    _crear_tablas_auxiliares()

    print("Base de datos inicializada con SQLAlchemy")

def _crear_tablas_auxiliares() -> None:
    from sqlalchemy import text
    
    with _engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """))
        
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
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        """))
        
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
    if _scoped_session is None:
        init_db()
    return _scoped_session()


def close_session() -> None:
    if _scoped_session is not None:
        _scoped_session.remove()


def close_db() -> None:
    global _engine, _session_factory, _scoped_session
    
    if _scoped_session is not None:
        _scoped_session.remove()
        _scoped_session = None
    
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _session_factory = None
    
    print("Base de datos cerrada")
