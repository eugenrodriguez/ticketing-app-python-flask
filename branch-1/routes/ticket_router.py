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
    parameters:
      - name: incluir_incidentes
        in: query
        type: boolean
        required: false
        description: Incluir lista de incidentes asociados
    responses:
      200:
        description: Lista de tickets obtenida exitosamente
    """
    incluir_inc = request.args.get("incluir_incidentes", "false").lower() == "true"
    tickets = controller.listar_tickets(incluir_incidentes=incluir_inc)
    return jsonify({"exito": True, "datos": tickets}), 200


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def obtener_ticket(ticket_id):
    """
    Obtiene los detalles de un ticket con sus incidentes.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
      - name: incluir_incidentes
        in: query
        type: boolean
        required: false
        default: true
    responses:
      200:
        description: Ticket encontrado
      404:
        description: Ticket no encontrado
    """
    incluir_inc = request.args.get("incluir_incidentes", "true").lower() == "true"
    ticket = controller.obtener_ticket(ticket_id, incluir_incidentes=incluir_inc)
    if ticket:
        return jsonify({"exito": True, "datos": ticket}), 200
    return jsonify({"exito": False, "mensaje": "Ticket no encontrado"}), 404


@ticket_bp.route("", methods=["POST"])
def crear_ticket():
    """
    Crea un nuevo ticket con incidentes asociados (relación 1:N).
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
            incidentes:
              type: array
              description: Lista de incidentes asociados al ticket
              items:
                type: object
                properties:
                  descripcion:
                    type: string
                    example: "Pantalla no enciende"
                  categoria:
                    type: string
                    enum: ["Hardware", "Software", "Red", "Otro"]
                    example: "Hardware"
                  prioridad:
                    type: string
                    enum: ["Baja", "Media", "Alta", "Crítica"]
                    example: "Alta"
          required:
            - cliente_id
            - servicio_id
            - equipo_id
            - empleado_id
    responses:
      201:
        description: Ticket creado exitosamente
      400:
        description: Parámetros inválidos
    """
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
    """
    Agrega un nuevo incidente a un ticket existente.
    ---
    tags:
      - Tickets
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
              example: "Teclado no responde"
            categoria:
              type: string
              enum: ["Hardware", "Software", "Red", "Otro"]
            prioridad:
              type: string
              enum: ["Baja", "Media", "Alta", "Crítica"]
          required:
            - descripcion
            - categoria
            - prioridad
    responses:
      201:
        description: Incidente agregado exitosamente
      400:
        description: Parámetros inválidos
      404:
        description: Ticket no encontrado
    """
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
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            estado:
              type: string
              enum: ["Abierto", "En Progreso", "Cerrado", "Reabierto"]
          required:
            - estado
    responses:
      200:
        description: Estado actualizado exitosamente
      400:
        description: Estado inválido
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
    responses:
      200:
        description: Ticket reabierto exitosamente
      400:
        description: No se pudo reabrir
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
    responses:
      200:
        description: Tickets filtrados exitosamente
    """
    estado = request.args.get("estado")
    if not estado:
        return jsonify({"exito": False, "mensaje": "Parámetro 'estado' requerido"}), 400
    
    tickets = controller.filtrar_por_estado(estado)
    return jsonify({"exito": True, "datos": tickets}), 200