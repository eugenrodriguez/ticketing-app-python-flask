from flask import Blueprint, request, jsonify
from controllers.incidente_controller import IncidenteController


incidente_bp = Blueprint("incidentes", __name__)
controller = IncidenteController()


@incidente_bp.get("/")
def listar_incidentes():
    """Listar incidentes
    ---
    tags:
      - Incidentes
    responses:
      200:
        description: Lista de incidentes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              descripcion:
                type: string
              categoria:
                type: string
              prioridad:
                type: string
    """
    return jsonify(controller.listar())


@incidente_bp.post("/")
def crear_incidente():
    """Crear incidente
    ---
    tags:
      - Incidentes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [descripcion, categoria, prioridad]
          properties:
            descripcion:
              type: string
            categoria:
              type: string
            prioridad:
              type: string
    responses:
      201:
        description: Incidente creado
        schema:
          type: object
          properties:
            id:
              type: integer
    """
    data = request.get_json(force=True, silent=True) or {}
    new_id = controller.crear(
        data.get("descripcion", ""), data.get("categoria", ""), data.get("prioridad", "")
    )
    return jsonify({"id": new_id}), 201


@incidente_bp.get("/<int:incidente_id>")
def obtener_incidente(incidente_id: int):
    """Obtener incidente por ID
    ---
    tags:
      - Incidentes
    parameters:
      - in: path
        name: incidente_id
        type: integer
        required: true
    responses:
      200:
        description: Incidente
      404:
        description: No encontrado
    """
    inc = controller.obtener(incidente_id)
    if not inc:
        return jsonify({"detail": "Incidente no encontrado"}), 404
    return jsonify(inc)


@incidente_bp.delete("/<int:incidente_id>")
def eliminar_incidente(incidente_id: int):
    """Eliminar incidente
    ---
    tags:
      - Incidentes
    parameters:
      - in: path
        name: incidente_id
        type: integer
        required: true
    responses:
      204:
        description: Eliminado
      404:
        description: No encontrado
    """
    ok = controller.eliminar(incidente_id)
    if not ok:
        return jsonify({"detail": "Incidente no encontrado"}), 404
    return ("", 204)


