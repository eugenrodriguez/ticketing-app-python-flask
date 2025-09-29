from flask import Flask
from flasgger import Swagger
from routes.incidente_router import incidente_bp
from routes.ticket_router import ticket_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Configuración básica de Swagger (Flasgger)
    app.config["SWAGGER"] = {
        "title": "Ticketing API",
        "uiversion": 3,
    }
    Swagger(app)

    # Registrar blueprints
    app.register_blueprint(incidente_bp, url_prefix="/incidentes")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")

    @app.route("/")
    def root():
        return {"name": "Ticketing API", "docs": "/apidocs"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)


