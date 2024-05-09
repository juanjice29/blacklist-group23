from flask import jsonify, request, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.blacklist.alta_blacklist import AltaBlacklist
from ..commands.blacklist.consulta_blacklist import ConsultaBlacklist

blacklist_blueprint = Blueprint('blacklist', __name__)

@blacklist_blueprint.route('/blacklist', methods = ['POST'])
@jwt_required()
def crear():
    json = request.get_json()
    current_app.logger.info(json)
    ip_peticion = request.remote_addr
    usuario = get_jwt_identity()
    current_app.logger.info('Usuario es : %s ip de la peticion: %s', str(usuario), str(ip_peticion))
    result = AltaBlacklist(json.get("email"), json.get("app_uuid"), json.get("blocked_reason"), usuario, ip_peticion).execute()
    current_app.logger.info(result)
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@blacklist_blueprint.route('/blacklist/<string:email>', methods = ['GET'])
@jwt_required()
def consulta(email):
    current_app.logger.info('Consulta correo es : %s', str(email))
    result = ConsultaBlacklist(email).execute()
    current_app.logger.info(result)
    return result[0], result[1]