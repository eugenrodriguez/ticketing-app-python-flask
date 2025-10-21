from flask import Blueprint, request, jsonify
from controllers.incidente_controller import IncidenteController

incidente_bp = Blueprint("incidentes", __name__)
controller = IncidenteController()


@incidente_bp.route("", methods=["GET"])
def listar_incidentes():
    """
    Obtiene la lista de todos los incidentes.
    ---
    tags:
      - Incidentes
    responses:
      200:
        description: Lista de incidentes obtenida exitosamente
    """
    incidentes = controller.listar_incidentes()
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/ticket/<int:ticket_id>", methods=["GET"])
def listar_incidentes_por_ticket(ticket_id):
    """
    Obtiene todos los incidentes de un ticket específico.
    ---
    tags:
      - Incidentes
    parameters:
      - name: ticket_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Incidentes del ticket
    """
    incidentes = controller.listar_incidentes_por_ticket(ticket_id)
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/<int:incidente_id>", methods=["GET"])
def obtener_incidente(incidente_id):
    """
    Obtiene los detalles de un incidente específico.
    ---
    tags:
      - Incidentes
    parameters:
      - name: incidente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Incidente encontrado
      404:
        description: Incidente no encontrado
    """
    incidente = controller.obtener_incidente(incidente_id)
    if incidente:
        return jsonify({"exito": True, "datos": incidente}), 200
    return jsonify({"exito": False, "mensaje": "Incidente no encontrado"}), 404


@incidente_bp.route("", methods=["POST"])
def crear_incidente():
    """
    Crea un nuevo incidente asociado a un ticket.
    ---
    tags:
      - Incidentes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
              example: "Pantalla no enciende"
            categoria:
              type: string
              enum: ["Hardware", "Software", "Red", "Otro"]
            prioridad:
              type: string
              enum: ["Baja", "Media", "Alta", "Crítica"]
            ticket_id:
              type: integer
              example: 1
          required:
            - descripcion
            - categoria
            - prioridad
            - ticket_id
    responses:
      201:
        description: Incidente creado exitosamente
      400:
        description: Parámetros inválidos
    """
    datos = request.get_json()
    
    if not datos or not all(k in datos for k in ["descripcion", "categoria", "prioridad", "ticket_id"]):
        return jsonify({"exito": False, "mensaje": "Faltan parámetros requeridos"}), 400
    
    resultado = controller.crear_incidente(
        descripcion=datos["descripcion"],
        categoria=datos["categoria"],
        prioridad=datos["prioridad"],
        ticket_id=datos["ticket_id"],
    )
    
    if resultado["exito"]:
        return jsonify(resultado), 201
    return jsonify(resultado), 400


@incidente_bp.route("/<int:incidente_id>", methods=["DELETE"])
def eliminar_incidente(incidente_id):
    """
    Elimina un incidente.
    ---
    tags:
      - Incidentes
    parameters:
      - name: incidente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Incidente eliminado exitosamente
      404:
        description: Incidente no encontrado
    """
    resultado = controller.eliminar_incidente(incidente_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 404


@incidente_bp.route("/filtrar/categoria", methods=["GET"])
def filtrar_por_categoria():
    """
    Filtra incidentes por categoría.
    ---
    tags:
      - Incidentes
    parameters:
      - name: categoria
        in: query
        type: string
        required: true
        enum: ["Hardware", "Software", "Red", "Otro"]
    responses:
      200:
        description: Incidentes filtrados exitosamente
    """
    categoria = request.args.get("categoria")
    if not categoria:
        return jsonify({"exito": False, "mensaje": "Parámetro 'categoria' requerido"}), 400
    
    incidentes = controller.filtrar_por_categoria(categoria)
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/filtrar/prioridad", methods=["GET"])
def filtrar_por_prioridad():
    """
    Filtra incidentes por prioridad.
    ---
    tags:
      - Incidentes
    parameters:
      - name: prioridad
        in: query
        type: string
        required: true
        enum: ["Baja", "Media", "Alta", "Crítica"]
    responses:
      200:
        description: Incidentes filtrados exitosamente
    """
    prioridad = request.args.get("prioridad")
    if not prioridad:
        return jsonify({"exito": False, "mensaje": "Parámetro 'prioridad' requerido"}), 400
    
    incidentes = controller.filtrar_por_prioridad(prioridad)
    return jsonify({"exito": True, "datos": incidentes}), 200