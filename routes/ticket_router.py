from flask import Blueprint, request, jsonify
from controllers.ticket_controller import TicketController


ticket_bp = Blueprint("tickets", __name__)
controller = TicketController()


@ticket_bp.post("/")
def crear_ticket():
    """Crear ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [cliente, servicio, equipo, empleado, incidente]
          properties:
            cliente:
              type: object
              required: [nombre, email, telefono, direccion]
              properties:
                nombre: {type: string}
                email: {type: string}
                telefono: {type: string}
                direccion: {type: string}
            servicio:
              type: object
              required: [nombre]
              properties:
                nombre: {type: string}
            equipo:
              type: object
              required: [descripcion, categoria, marca, modelo, nro_serie]
              properties:
                descripcion: {type: string}
                categoria: {type: string}
                marca: {type: string}
                modelo: {type: string}
                nro_serie: {type: string}
            empleado:
              type: object
              required: [nombre, categoria, rol]
              properties:
                nombre: {type: string}
                categoria: {type: string}
                rol: {type: string}
            incidente:
              type: object
              required: [descripcion, categoria, prioridad]
              properties:
                id: {type: integer}
                descripcion: {type: string}
                categoria: {type: string}
                prioridad: {type: string}
            fecha_creacion: {type: string}
    responses:
      201:
        description: Ticket creado
        schema:
          type: object
          properties:
            id: {type: integer}
    """
    payload = request.get_json(force=True, silent=True) or {}
    ticket_id = controller.crear_ticket(
        cliente=payload.get("cliente", {}),
        servicio=payload.get("servicio", {}),
        equipo=payload.get("equipo", {}),
        empleado=payload.get("empleado", {}),
        incidente=payload.get("incidente", {}),
        fecha_creacion=payload.get("fecha_creacion"),
    )
    return jsonify({"id": ticket_id}), 201


@ticket_bp.post("/<int:ticket_id>/reabrir")
def reabrir_ticket(ticket_id: int):
    """Reabrir ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: Reabierto
      400:
        description: No se puede reabrir
    """
    ok = controller.reabrir_ticket(ticket_id)
    if not ok:
        return jsonify({"detail": "No se puede reabrir (no existe o no está cerrado)"}), 400
    return jsonify({"ok": True})


@ticket_bp.post("/<int:ticket_id>/trabajos")
def agregar_trabajo(ticket_id: int):
    """Agregar trabajo al ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [autor, contenido]
          properties:
            autor: {type: string}
            contenido: {type: string}
            fecha: {type: string}
    responses:
      201:
        description: Trabajo creado
        schema:
          type: object
          properties:
            id: {type: integer}
      404:
        description: Ticket no encontrado
    """
    payload = request.get_json(force=True, silent=True) or {}
    try:
        trabajo_id = controller.agregar_trabajo(
            ticket_id,
            payload.get("autor", ""),
            payload.get("contenido", ""),
            payload.get("fecha"),
        )
        return jsonify({"id": trabajo_id}), 201
    except ValueError:
        return jsonify({"detail": "Ticket no encontrado"}), 404


@ticket_bp.get("/<int:ticket_id>")
def obtener_ticket(ticket_id: int):
    """Obtener ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: Ticket
      404:
        description: No encontrado
    """
    tk = controller.obtener_ticket(ticket_id)
    if not tk:
        return jsonify({"detail": "Ticket no encontrado"}), 404
    return jsonify(tk)


@ticket_bp.get("/<int:ticket_id>/historial")
def historial_ticket(ticket_id: int):
    """Ver historial del ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: Historial
    """
    return jsonify(controller.ver_historial(ticket_id))


