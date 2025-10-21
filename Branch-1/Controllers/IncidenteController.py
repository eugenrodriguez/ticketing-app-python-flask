from flask import jsonify

class IncidenteController:
    def __init__(self, app, model):
        self.app = app
        self.model = model
        
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route("/incidente/crear/<num_ticket>/<tipo>/<descripcion>")
        def crear_incidente(num_ticket, tipo, descripcion):
            self.model.crear(num_ticket, tipo, descripcion)
            return "ticket creado"
            
            
        @self.app.route("/incidente/listar")
        def listar_incidentes():
            incidentes = self.model.listar()
            return jsonify([incidente.to_dict() for incidente in incidentes])
        
        
        @self.app.route("/incidente/buscar/<id>")
        def buscar_incidente(id):
            incidente = self.model.buscar(id)
            
            if incidente:
                return jsonify(incidente.to_dict())
            else:
                return "incidente no encontrado"
        
        
        @self.app.route("/incidente/borrar/<id>")
        def borrar_incidente(id):
            self.model.borrar(id)
            
            return "incidente borrado"
        
        @self.app.route("/incidente/modificar/<int:id>/<tipo>/<descripcion>")
        def modificar_incidente(id, tipo, descripcion):
            exito = self.model.modificar(id, tipo=tipo, descripcion=descripcion)

            if exito:
                return f"Incidente {id} modificado correctamente"
            else:
                return "Incidente no encontrado"