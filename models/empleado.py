class Empleado:
    def __init__(self, id: int, nombre: str, categoria: str, rol: str):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.rol = rol


class Tecnico(Empleado):
    def __init__(self, id: int, nombre: str, especialidad: str):
        super().__init__(id, nombre, categoria="Técnico", rol="Soporte Técnico")
        self.especialidad = especialidad


class OperadorTelefonico(Empleado):
    def __init__(self, id: int, nombre: str, turno: str):
        super().__init__(id, nombre, categoria="Operador", rol="Atención Telefónica")
        self.turno = turno
