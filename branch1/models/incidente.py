from database.db import db

class Incidente(db.Model):
    __tablename__ = 'incidentes'
    id = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'detalle': self.detalle,
            'estado': self.estado,
            'ticket_id': self.ticket_id
        }
