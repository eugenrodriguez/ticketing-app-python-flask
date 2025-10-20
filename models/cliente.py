class Cliente:
    def __init__(self, id: int, nombre: str, email: str, telefono: str, direccion: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.tickets = []
