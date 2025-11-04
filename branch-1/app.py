from flask import Flask, jsonify
from flasgger import Swagger
from routes.incidente_router import incidente_bp
from routes.ticket_router import ticket_bp
from database.db import init_db, close_session, close_db


def create_app() -> Flask:
    app = Flask(__name__)
    
    with app.app_context():
        init_db()
    
    app.config["SWAGGER"] = {
        "title": "Ticketing API",
        "uiversion": 3,
        "version": "2.0.0",
    }
    
    swagger = Swagger(app, template_file="swagger_docs.yml")
    
    app.register_blueprint(incidente_bp, url_prefix="/incidentes")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    
    @app.route("/", methods=["GET"])
    def root():
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
        return jsonify({
            "status": "healthy",
            "mensaje": "La API está funcionando correctamente",
            "database": "SQLite con SQLAlchemy ORM",
        }), 200
    
    @app.errorhandler(404)
    def no_encontrado(error):
        return jsonify({
            "exito": False,
            "mensaje": "Recurso no encontrado",
        }), 404
    
    @app.errorhandler(500)
    def error_interno(error):
        return jsonify({
            "exito": False,
            "mensaje": "Error interno del servidor",
            "detalle": str(error),
        }), 500
    
    @app.teardown_appcontext
    def cleanup(exception=None):
        close_session()
    
    return app


app = create_app()


if __name__ == "__main__":
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
