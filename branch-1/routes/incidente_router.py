from flask import Blueprint, request, jsonify
from controllers.incidente_controller import IncidenteController

incidente_bp = Blueprint("incidentes", __name__)
controller = IncidenteController()


@incidente_bp.route("", methods=["GET"])
def listar_incidentes():
    incidentes = controller.listar_incidentes()
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/ticket/<int:ticket_id>", methods=["GET"])
def listar_incidentes_por_ticket(ticket_id):
    incidentes = controller.listar_incidentes_por_ticket(ticket_id)
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/<int:incidente_id>", methods=["GET"])
def obtener_incidente(incidente_id):
    incidente = controller.obtener_incidente(incidente_id)
    if incidente:
        return jsonify({"exito": True, "datos": incidente}), 200
    return jsonify({"exito": False, "mensaje": "Incidente no encontrado"}), 404


@incidente_bp.route("", methods=["POST"])
def crear_incidente():
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
    resultado = controller.eliminar_incidente(incidente_id)
    if resultado["exito"]:
        return jsonify(resultado), 200
    return jsonify(resultado), 404


@incidente_bp.route("/filtrar/categoria", methods=["GET"])
def filtrar_por_categoria():
    categoria = request.args.get("categoria")
    if not categoria:
        return jsonify({"exito": False, "mensaje": "Parámetro 'categoria' requerido"}), 400
    
    incidentes = controller.filtrar_por_categoria(categoria)
    return jsonify({"exito": True, "datos": incidentes}), 200


@incidente_bp.route("/filtrar/prioridad", methods=["GET"])
def filtrar_por_prioridad():
    prioridad = request.args.get("prioridad")
    if not prioridad:
        return jsonify({"exito": False, "mensaje": "Parámetro 'prioridad' requerido"}), 400
    
    incidentes = controller.filtrar_por_prioridad(prioridad)
    return jsonify({"exito": True, "datos": incidentes}), 200