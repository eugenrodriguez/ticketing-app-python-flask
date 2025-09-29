from datetime import datetime

class Ticket:
    def __init__(self, id: int, cliente, servicio, equipo, empleado, incidente):
        self.id = id
        self.cliente = cliente
        self.servicio = servicio
        self.equipo = equipo
        self.empleado = empleado
        self.incidente = incidente
        self.estado = "Abierto"
        self.fecha_creacion = datetime.now()
        self.fecha_cierre = None
        self.mensajes = []

    def cerrar_ticket(self):
        self.estado = "Cerrado"
        self.fecha_cierre = datetime.now()

    def reabrir_ticket(self):
        if self.estado == "Cerrado":
            self.estado = "Reabierto"
            self.fecha_cierre = None
