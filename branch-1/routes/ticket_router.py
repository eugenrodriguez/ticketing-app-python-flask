from flask import Blueprint, request, jsonify
from controllers.ticket_controller import TicketController

ticket_bp = Blueprint("tickets", __name__)
controller = TicketController()


@ticket_bp.route("", methods=["GET"])
def listar_tickets():
    incluir_inc = request.args.get("incluir_incidentes", "false").lower() == "true"
    tickets = controller.listar_tickets(incluir_incidentes=incluir_inc)
    return jsonify({"exito": True, "datos": tickets}), 200


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def obtener_ticket(ticket_id):
    incluir_inc = request.args.get("incluir_incidentes", "true").lower() == "true"
    ticket = controller.obtener_ticket(ticket_id, incluir_incidentes=incluir_inc)
    if ticket:
        return jsonify({"exito": True, "datos": ticket}), 200
    return jsonify({"exito": False, "mensaje": "Ticket no encontrado"}), 404


@ticket_bp.route("", methods=["POST"])
def crear_ticket():
    datos = request.get_json()
    
    campos_requeridos = ["cliente_id", "servicio_id", "equipo_id", "empleado_id"]
    if not datos or not all(k in datos for k in campos_requeridos):
        return jsonify({"exito": False, "mensaje": "Faltan parámetros requeridos"}), 400
    
    resultado = controller.crear_ticket(
        cliente_id=datos["cliente_id"],
        servicio_id=datos["servicio_id"],
        equipo_id=datos["equipo_id"],
        empleado_id=datos["empleado_id"],
        incidentes_data=datos.get("incidentes", []),
    )
    
    return jsonify(resultado), 201


@ticket_bp.route("/<int:ticket_id>/incidentes", methods=["POST"])
def agregar_incidente_a_ticket(ticket_id):
    datos = request.get_json()
    
    if not datos or not all(k in datos for k in ["descripcion", "categoria", "prioridad"]):
        return jsonify({"exito": False, "mensaje": "Faltan parámetros requeridos"}), 400
    
    resultado = controller.agregar_incidente_a_ticket(
        ticket_id=ticket_id,
        descripcion=datos["descripcion"],
        categoria=datos["categoria"],
        prioridad=datos["prioridad"],
    )
    
    if resultado["exito"]:
        return jsonify(resultado), 201
    return jsonify(resultado), 404


@ticket_bp.route("/<int:ticket_id>/estado", methods=["PUT"])
def cambiar_estado_ticket(ticket_id):
    datos = request.get_json()
    
    if not datos or "estado" not in datos:
        return jsonify({"exito": False, "mensaje": "Parámetro 'estado' requerido"}), 400
    
    resultado = controller.cambiar_estado_ticket(ticket_id, datos["estado"])
    
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 400


@ticket_bp.route("/<int:ticket_id>/cerrar", methods=["PUT"])
def cerrar_ticket(ticket_id):
    resultado = controller.cerrar_ticket(ticket_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 404


@ticket_bp.route("/<int:ticket_id>/reabrir", methods=["PUT"])
def reabrir_ticket(ticket_id):
    resultado = controller.reabrir_ticket(ticket_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 400


@ticket_bp.route("/filtrar/estado", methods=["GET"])
def filtrar_por_estado():
    estado = request.args.get("estado")
    if not estado:
        return jsonify({"exito": False, "mensaje": "Parámetro 'estado' requerido"}), 400
    
    tickets = controller.filtrar_por_estado(estado)
    return jsonify({"exito": True, "datos": tickets}), 200