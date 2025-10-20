from flask import Blueprint, request, jsonify
from controllers.ticket_controller import TicketController

ticket_bp = Blueprint("tickets", __name__)
controller = TicketController()


@ticket_bp.route("", methods=["GET"])
def listar_tickets():
    """
    Obtiene la lista de todos los tickets.
    ---
    tags:
      - Tickets
    responses:
      200:
        description: Lista de tickets obtenida exitosamente
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              cliente_id:
                type: integer
              servicio_id:
                type: integer
              equipo_id:
                type: integer
              empleado_id:
                type: integer
              incidente_id:
                type: integer
              estado:
                type: string
              fecha_creacion:
                type: string
              fecha_cierre:
                type: string
    """
    tickets = controller.listar_tickets()
    return jsonify({"exito": True, "datos": tickets}), 200


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def obtener_ticket(ticket_id):
    """
    Obtiene los detalles de un ticket específico.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: ID del ticket
    responses:
      200:
        description: Ticket encontrado
        schema:
          type: object
      404:
        description: Ticket no encontrado
    """
    ticket = controller.obtener_ticket(ticket_id)
    if ticket:
        return jsonify({"exito": True, "datos": ticket}), 200
    return jsonify({"exito": False, "mensaje": "Ticket no encontrado"}), 404


@ticket_bp.route("", methods=["POST"])
def crear_ticket():
    """
    Crea un nuevo ticket.
    ---
    tags:
      - Tickets
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            cliente_id:
              type: integer
              example: 1
            servicio_id:
              type: integer
              example: 1
            equipo_id:
              type: integer
              example: 1
            empleado_id:
              type: integer
              example: 1
            incidente_id:
              type: integer
              example: 1
          required:
            - cliente_id
            - servicio_id
            - equipo_id
            - empleado_id
            - incidente_id
    responses:
      201:
        description: Ticket creado exitosamente
        schema:
          type: object
          properties:
            id:
              type: integer
            mensaje:
              type: string
            estado:
              type: string
      400:
        description: Parámetros inválidos
    """
    datos = request.get_json()
    
    campos_requeridos = ["cliente_id", "servicio_id", "equipo_id", "empleado_id", "incidente_id"]
    if not datos or not all(k in datos for k in campos_requeridos):
        return jsonify({"exito": False, "mensaje": "Faltan parámetros requeridos"}), 400
    
    resultado = controller.crear_ticket(
        cliente_id=datos["cliente_id"],
        servicio_id=datos["servicio_id"],
        equipo_id=datos["equipo_id"],
        empleado_id=datos["empleado_id"],
        incidente_id=datos["incidente_id"],
    )
    
    return jsonify(resultado), 201


@ticket_bp.route("/<int:ticket_id>/estado", methods=["PUT"])
def cambiar_estado_ticket(ticket_id):
    """
    Cambia el estado de un ticket.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: ID del ticket
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            estado:
              type: string
              enum: ["Abierto", "En Progreso", "Cerrado", "Reabierto"]
              example: "En Progreso"
          required:
            - estado
    responses:
      200:
        description: Estado actualizado exitosamente
      400:
        description: Estado inválido
      404:
        description: Ticket no encontrado
    """
    datos = request.get_json()
    
    if not datos or "estado" not in datos:
        return jsonify({"exito": False, "mensaje": "Parámetro 'estado' requerido"}), 400
    
    resultado = controller.cambiar_estado_ticket(ticket_id, datos["estado"])
    
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 400


@ticket_bp.route("/<int:ticket_id>/cerrar", methods=["PUT"])
def cerrar_ticket(ticket_id):
    """
    Cierra un ticket registrando la fecha de cierre.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: ID del ticket a cerrar
    responses:
      200:
        description: Ticket cerrado exitosamente
      404:
        description: Ticket no encontrado
    """
    resultado = controller.cerrar_ticket(ticket_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 404


@ticket_bp.route("/<int:ticket_id>/reabrir", methods=["PUT"])
def reabrir_ticket(ticket_id):
    """
    Reabre un ticket cerrado.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
        description: ID del ticket a reabrir
    responses:
      200:
        description: Ticket reabierto exitosamente
      400:
        description: No se pudo reabrir (no está cerrado)
      404:
        description: Ticket no encontrado
    """
    resultado = controller.reabrir_ticket(ticket_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 400


@ticket_bp.route("/filtrar/estado", methods=["GET"])
def filtrar_por_estado():
    """
    Filtra tickets por estado.
    ---
    tags:
      - Tickets
    parameters:
      - name: estado
        in: query
        type: string
        required: true
        enum: ["Abierto", "En Progreso", "Cerrado", "Reabierto"]
        description: Estado del ticket
    responses:
      200:
        description: Tickets filtrados exitosamente
        schema:
          type: array
          items:
            type: object
    """
    estado = request.args.get("estado")
    if not estado:
        return jsonify({"exito": False, "mensaje": "Parámetro 'estado' requerido"}), 400
    
    tickets = controller.filtrar_por_estado(estado)
    return jsonify({"exito": True, "datos": tickets}), 200