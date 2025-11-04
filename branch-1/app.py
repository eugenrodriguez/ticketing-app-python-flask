"""
Ticketing API - Aplicación principal con SQLAlchemy
Sistema de gestión de tickets para reparaciones con relación 1:N
"""

from flask import Flask, jsonify
from flasgger import Swagger
from routes.incidente_router import incidente_bp
from routes.ticket_router import ticket_bp
from database.db import init_db, close_session, close_db


def create_app() -> Flask:
    """Crea e inicializa la aplicación Flask con SQLAlchemy."""
    app = Flask(__name__)
    
    # Inicializar base de datos con SQLAlchemy
    with app.app_context():
        init_db()
    
    # Configuración de Swagger/Flasgger
    app.config["SWAGGER"] = {
        "title": "Ticketing API",
        "uiversion": 3,
        "version": "2.0.0",
    }
    
    # Cargar especificación desde el archivo YAML
    swagger = Swagger(app, template_file="swagger_docs.yml")
    
    # Registrar blueprints con prefijos
    app.register_blueprint(incidente_bp, url_prefix="/incidentes")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    
    # Rutas raíz
    @app.route("/", methods=["GET"])
    def root():
        """Endpoint raíz de la API."""
        return jsonify({
            "nombre": "Ticketing API con SQLAlchemy",
            "version": "2.0.0",
            "orm": "SQLAlchemy",
            "relacion": "1 Ticket → N Incidentes",
            "documentacion": "/apidocs",
            "endpoints": {
                "incidentes": "/incidentes",
                "tickets": "/tickets",
            },
        }), 200
    
    @app.route("/health", methods=["GET"])
    def health():
        """Verificar estado de la API."""
        return jsonify({
            "status": "healthy",
            "mensaje": "La API está funcionando correctamente",
            "database": "SQLite con SQLAlchemy ORM",
        }), 200
    
    # Manejador de errores global
    @app.errorhandler(404)
    def no_encontrado(error):
        """Manejo de rutas no encontradas."""
        return jsonify({
            "exito": False,
            "mensaje": "Recurso no encontrado",
        }), 404
    
    @app.errorhandler(500)
    def error_interno(error):
        """Manejo de errores internos del servidor."""
        return jsonify({
            "exito": False,
            "mensaje": "Error interno del servidor",
            "detalle": str(error),
        }), 500
    
    # Cleanup al cerrar
    @app.teardown_appcontext
    def cleanup(exception=None):
        """Cierra sesiones de SQLAlchemy al finalizar."""
        close_session()
    
    return app


# Crear instancia de la app
app = create_app()


if __name__ == "__main__":
    # Ejecutar servidor de desarrollo
    print("=" * 60)
    print(" Iniciando Ticketing API con SQLAlchemy")
    print("=" * 60)
    print(" URL: http://127.0.0.1:8000")
    print(" Swagger: http://127.0.0.1:8000/apidocs")
    print("  Health: http://127.0.0.1:8000/health")
    print(" Relación: 1 Ticket → N Incidentes")
    print("=" * 60)
    
    try:
        app.run(
            host="127.0.0.1",
            port=8000,
            debug=True,
            use_reloader=True,
        )
    finally:
        close_db()