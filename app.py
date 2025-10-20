"""
Ticketing API - Aplicación principal
Sistema de gestión de tickets para reparaciones
"""

from flask import Flask, jsonify
from flasgger import Swagger
from routes.incidente_router import incidente_bp
from routes.ticket_router import ticket_bp
from database.db import close_connection


def create_app() -> Flask:
    """Crea e inicializa la aplicación Flask."""
    app = Flask(__name__)
    
    # Configuración de Swagger/Flasgger
    app.config["SWAGGER"] = {
        "title": "Ticketing API",
        "uiversion": 3,
        "version": "1.0.0",
    }
    
    swagger = Swagger(app, template={
        "info": {
            "title": "Sistema de Ticketing",
            "description": "API para gestión de tickets de servicio técnico",
            "version": "1.0.0",
        },
        "tags": [
            {
                "name": "Tickets",
                "description": "Operaciones relacionadas con tickets",
            },
            {
                "name": "Incidentes",
                "description": "Operaciones relacionadas con incidentes",
            },
        ],
    })
    
    # Registrar blueprints con prefijos
    app.register_blueprint(incidente_bp, url_prefix="/incidentes")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    
    # Rutas raíz
    @app.route("/", methods=["GET"])
    def root():
        """Endpoint raíz de la API."""
        return jsonify({
            "nombre": "Ticketing API",
            "version": "1.0.0",
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
        }), 500
    
    # Cleanup al cerrar
    @app.teardown_appcontext
    def cleanup(exception=None):
        """Cierra conexiones al finalizar la app."""
        close_connection()
    
    return app


# Crear instancia de la app
app = create_app()


if __name__ == "__main__":
    # Ejecutar servidor de desarrollo
    print("Iniciando Ticketing API en http://127.0.0.1:8000")
    print("Documentación en http://127.0.0.1:8000/apidocs")
    print("Health check en http://127.0.0.1:8000/health")
    
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True,
        use_reloader=True,
    )