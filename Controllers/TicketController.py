from flask import jsonify

class TicketController:
    def __init__(self, app, model):
        self.app = app
        self.model = model
        
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route("/ticket/crear/<cliente>/<operador>/<equipo>")
        def crear_ticket(cliente, operador, equipo):
            mensaje = "ticket registrado"
            estado = False
            
            self.model.crear(cliente, operador, equipo, mensaje, estado)
            return "ticket creado"
        
        @self.app.route("/ticket/listar")
        def listar_ticket():
            tickets = self.model.listar()
            # return jsonify(tickets)
            return jsonify([t.to_dict() for t in tickets])
            
        @self.app.route("/ticket/buscar/<id>")
        def buscar_ticket(id):
            ticket = self.model.buscar(id)
            
            if ticket:
                return jsonify([ticket.to_dict()])
            else:
                return "Ticket no encontrado"
            
        @self.app.route("/ticket/borrar/<id>")
        def borrar_ticket(id):
            self.model.borrar(id)
            return "ticket eliminado"
        
        @self.app.route("/ticket/modificar/<int:id>/<cliente>/<operador>/<equipo>/<mensaje>/<estado>")
        def modificar_ticket(id, cliente, operador, equipo, mensaje, estado):
            estado_bool = estado.lower() == "true"

            exito = self.model.modificar(
                id=id,
                cliente=cliente,
                operador=operador,
                equipo=equipo,
                mensaje=mensaje,
                estado=estado_bool
            )

            if exito:
                return f"Ticket {id} modificado correctamente"
            else:
                return"Ticket no encontrado"