from datetime import datetime

class Mensaje:
    def __init__(self, id: int, ticket, autor: str, contenido: str):
        self.id = id
        self.ticket = ticket
        self.autor = autor
        self.contenido = contenido
        self.fecha_envio = datetime.now()
