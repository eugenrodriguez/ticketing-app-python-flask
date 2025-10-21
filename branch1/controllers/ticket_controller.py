from flask import request, abort
from flask_restful import Resource
from database.db import db
from models.ticket import Ticket
from models.incidente import Incidente
from flasgger import swag_from

class TicketListResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'List of tickets',
                'schema': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/Ticket'}
                }
            }
        }
    })
    def get(self):
        tickets = Ticket.query.all()
        return [t.to_dict() for t in tickets], 200

    @swag_from({
        'parameters': [
            {'name':'titulo','in':'formData','type':'string','required':True},
            {'name':'descripcion','in':'formData','type':'string','required':False}
        ],
        'responses': {201: {'description': 'Ticket created'}}
    })
    def post(self):
        data = request.get_json() or request.form
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        if not titulo:
            abort(400, 'titulo es requerido')
        ticket = Ticket(titulo=titulo, descripcion=descripcion)
        db.session.add(ticket)
        db.session.commit()
        return ticket.to_dict(), 201

class TicketResource(Resource):
    @swag_from({
        'responses': {200: {'description':'Ticket found','schema': {'$ref':'#/definitions/Ticket'}}}
    })
    def get(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        data = ticket.to_dict()
        data['incidentes'] = [i.to_dict() for i in ticket.incidentes]
        return data, 200

    def put(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json() or request.form
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        if titulo:
            ticket.titulo = titulo
        if descripcion is not None:
            ticket.descripcion = descripcion
        db.session.commit()
        return ticket.to_dict(), 200

    def delete(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        return {'message':'deleted'}, 200

class TicketIncidentesResource(Resource):
    @swag_from({
        'responses': {200: {'description':'List incidents for ticket'}}
    })
    def get(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        return [i.to_dict() for i in ticket.incidentes], 200

    @swag_from({
        'parameters': [
            {'name':'detalle','in':'formData','type':'string','required':True},
            {'name':'estado','in':'formData','type':'string','required':False}
        ],
        'responses': {201: {'description':'Incidente creado'}}
    })
    def post(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json() or request.form
        detalle = data.get('detalle')
        estado = data.get('estado') or 'pendiente'
        if not detalle:
            abort(400, 'detalle es requerido')
        incidente = Incidente(detalle=detalle, estado=estado, ticket_id=ticket.id)
        db.session.add(incidente)
        db.session.commit()
        return incidente.to_dict(), 201
