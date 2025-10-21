from flask import request
from flask_restful import Resource
from database.db import db
from models.incidente import Incidente
from flasgger import swag_from

class IncidenteResource(Resource):
    def get(self, incidente_id):
        incidente = Incidente.query.get_or_404(incidente_id)
        return incidente.to_dict(), 200

    def put(self, incidente_id):
        incidente = Incidente.query.get_or_404(incidente_id)
        data = request.get_json() or request.form
        detalle = data.get('detalle')
        estado = data.get('estado')
        if detalle:
            incidente.detalle = detalle
        if estado:
            incidente.estado = estado
        db.session.commit()
        return incidente.to_dict(), 200

    def delete(self, incidente_id):
        incidente = Incidente.query.get_or_404(incidente_id)
        db.session.delete(incidente)
        db.session.commit()
        return {'message':'deleted'}, 200
