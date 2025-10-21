from flask import Flask, jsonify
from flask_restful import Api
from flasgger import Swagger
from database.db import db, init_db
from controllers.ticket_controller import TicketListResource, TicketResource, TicketIncidentesResource
from controllers.incidente_controller import IncidenteResource

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    Swagger(app)
    api = Api(app)

    db.init_app(app)
    with app.app_context():
        init_db()

    api.add_resource(TicketListResource, '/tickets')
    api.add_resource(TicketResource, '/tickets/<int:ticket_id>')
    api.add_resource(TicketIncidentesResource, '/tickets/<int:ticket_id>/incidentes')
    api.add_resource(IncidenteResource, '/incidentes/<int:incidente_id>')

    @app.route('/health')
    def health():
        return jsonify({'status':'ok'})

    @app.route('/')
    def index():
        return jsonify({"message":"Ticketing API - visit /apidocs for Swagger UI"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
