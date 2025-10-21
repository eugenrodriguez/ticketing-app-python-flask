from DataBase.db import Sesion
from DataBase.Incidente import Incidente

class IncidenteModel:
    def __init__(self):
        self.sesion = Sesion()
        
    def crear(self, id_ticket, tipo, descripcion):
        incidente = Incidente(id_ticket=id_ticket, tipo=tipo, descripcion=descripcion)
        self.sesion.add(incidente)
        self.sesion.commit()
        
    def listar(self):
        return self.sesion.query(Incidente).all()
    
    def buscar(self, id):
        return self.sesion.get(Incidente, id)
    
    def borrar(self, id):
        incidente = self.sesion.get(Incidente, id)
        
        if incidente:
            self.sesion.delete(incidente)
            self.sesion.commit()
            return True
        
        else:
            return False
    
    def modificar(self, id, tipo=None, descripcion=None):
        incidente = self.sesion.get(Incidente, id)
        if not incidente:
            return False
        
        if tipo is not None:
            incidente.tipo = tipo
        if descripcion is not None:
            incidente.descripcion = descripcion

        self.sesion.commit()
        return True